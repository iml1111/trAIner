import os
import numpy as np
from typing import List
import torch
from controller.exceptions import (
    UserIndexError, ItemIndexError
)


class FeaturesLinear(torch.nn.Module):

    def __init__(self, field_dims, output_dim=1):
        super().__init__()
        self.fc = torch.nn.Embedding(sum(field_dims), output_dim)
        self.bias = torch.nn.Parameter(torch.zeros((output_dim,)))
        self.offsets = np.array((0, *np.cumsum(field_dims)[:-1]), dtype=np.long)

    def forward(self, x):
        """
        :param x: Long tensor of size ``(batch_size, num_fields)``
        """
        x = x + x.new_tensor(self.offsets).unsqueeze(0)
        return torch.sum(self.fc(x), dim=1) + self.bias


class FeaturesEmbedding(torch.nn.Module):

    def __init__(self, field_dims, embed_dim):
        super().__init__()
        self.embedding = torch.nn.Embedding(sum(field_dims), embed_dim)
        self.offsets = np.array((0, *np.cumsum(field_dims)[:-1]), dtype=np.long)
        torch.nn.init.xavier_uniform_(self.embedding.weight.data)

    def forward(self, x):
        """
        :param x: Long tensor of size ``(batch_size, num_fields)``
        """
        x = x + x.new_tensor(self.offsets).unsqueeze(0)
        return self.embedding(x)


class FactorizationMachine(torch.nn.Module):

    def __init__(self, reduce_sum=True):
        super().__init__()
        self.reduce_sum = reduce_sum

    def forward(self, x):
        """
        :param x: Float tensor of size ``(batch_size, num_fields, embed_dim)``
        """
        square_of_sum = torch.sum(x, dim=1) ** 2
        sum_of_square = torch.sum(x ** 2, dim=1)
        ix = square_of_sum - sum_of_square
        if self.reduce_sum:
            ix = torch.sum(ix, dim=1, keepdim=True)
        return 0.5 * ix


class MultiLayerPerceptron(torch.nn.Module):

    def __init__(self, input_dim, embed_dims, dropout, output_layer=True):
        super().__init__()
        layers = list()
        for embed_dim in embed_dims:
            layers.append(torch.nn.Linear(input_dim, embed_dim))
            layers.append(torch.nn.ReLU())
            layers.append(torch.nn.BatchNorm1d(embed_dim))
            #layers.append(torch.nn.Dropout(p=dropout))
            input_dim = embed_dim
        if output_layer:
            layers.append(torch.nn.Linear(input_dim, 1))
        self.mlp = torch.nn.Sequential(*layers)

    def forward(self, x):
        """
        :param x: Float tensor of size ``(batch_size, embed_dim)``
        """
        return self.mlp(x)


class DeepFactorizationMachineModel(torch.nn.Module):
    """
    A pytorch implementation of DeepFM.
    Reference:
        H Guo, et al. DeepFM: A Factorization-Machine based Neural Network for CTR Prediction, 2017.
    """

    def __init__(self, field_dims, embed_dim, mlp_dims, dropout):
        super().__init__()
        self.linear = FeaturesLinear(field_dims)
        self.fm = FactorizationMachine(reduce_sum=True)
        self.embedding = FeaturesEmbedding(field_dims, embed_dim)
        self.embed_output_dim = len(field_dims) * embed_dim
        self.mlp = MultiLayerPerceptron(self.embed_output_dim, mlp_dims, dropout=dropout)

    def forward(self, x):
        """
        :param x: Long tensor of size ``(batch_size, num_fields)``
        """
        embed_x = self.embedding(x)
        x = self.linear(x) + self.fm(embed_x) + self.mlp(embed_x.view(-1, self.embed_output_dim))
        return torch.sigmoid(x)


class DeepPredictor:

    def __init__(self, deep_model_path: str):
        self.deep_model_path = deep_model_path
        model_data = torch.load(
            deep_model_path,
            map_location=torch.device('cpu')
        )
        self.model_state_dict = model_data['model']
        self.model_config = model_data['config']
        self.model = DeepFactorizationMachineModel(
            # # Users: 1003, Items: 1188 (1003, 1188)
            [1003, 1188],
            self.model_config.embed_dim,
            self.model_config.mlp_dims,
            self.model_config.dropout,
        ).to('cpu')
        self.model.load_state_dict(self.model_state_dict)
        self.model.eval()

    def predict(self, user_id: int, item_id: int) -> float:

        if not (0 <= user_id <= 1002):
            raise UserIndexError()
        if not (0 <= item_id <= 1187):
            raise ItemIndexError()

        with torch.no_grad():
            x = torch.tensor([[user_id, item_id]])
            y = self.model(x)
        return float(y[0][0])

    def predict_multi(self, data: List[List[int]]) -> List[float]:
        """
        data = [
            [1, 1], # user_id, item_id
            [1, 2],
            [1, 3],
            ...
        ]
        """
        with torch.no_grad():
            x = torch.tensor(data)
            y = self.model(x)
        return [float(i[0]) for i in y]


if __name__ == '__main__':
    from config import config

    predictor = DeepPredictor(config.DEEP_MODEL_PATH)

    # (22,610) => 0.104762
    user_id, item_id = 22, 610
    print(predictor.predict(user_id, item_id))
    
    # (22,597) => 0.000000
    user_id, item_id = 22, 597
    print(predictor.predict(user_id, item_id))

    # 병렬 연산 예제
    print(predictor.predict_multi([[i, i] for i in range(1000)]))
