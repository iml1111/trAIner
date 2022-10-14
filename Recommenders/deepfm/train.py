import os
import argparse
from pprint import pprint
import torch
from torch import optim
import torch.nn as nn
from model import DeepFactorizationMachineModel
from data_loader import KMRDDataset, DataLoader
from trainer import Trainer
from dotenv import load_dotenv

load_dotenv(verbose=True)

KMRD_LARGE_DATA_PATH=os.environ['KMRD_LARGE_DATA_PATH']
KMRD_SMALL_DATA_PATH=os.environ['KMRD_SMALL_DATA_PATH']
KMRD_SUPER_LARGE_DATA_PATH=os.environ['KMRD_SUPER_LARGE_DATA_PATH']


def define_argparser():
    p = argparse.ArgumentParser()

    p.add_argument(
        '--model_fn',
        default='./model.pth',
        help='Model file name to save. Additional information would be annotated to the file name.'
    )
    p.add_argument(
        '--data_path',
        default=KMRD_LARGE_DATA_PATH,
        help='Dataset Path, Default=%(default)s'
    )
    p.add_argument(
        '--batch_size',
        type=int,
        default=256,
        help='Mini batch size for gradient descent. Default=%(default)s'
    )
    p.add_argument(
        '--n_epochs',
        type=int,
        default=30,
        help='Number of epochs to train. Default=%(default)s'
    )
    p.add_argument(
        '--embed_dim',
        type=int,
        default=16,
        help='Embedding Vector Size. Default=%(default)s'
    )
    p.add_argument(
        '--mlp_dims',
        type=list,
        default=[16, 16, 16],
        help='MultiLayerPerceptron Layers size. Default=%(default)s'
    )
    p.add_argument(
        '--train_ratio',
        type=float,
        default=0.8,
        help='Train data ratio. Default=%(default)s'
    )
    p.add_argument(
        '--valid_ratio',
        type=float,
        default=0.1,
        help='Valid data ratio. Default=%(default)s'
    )
    config = p.parse_args()
    return config


def main(config):
    print("# Config")
    pprint(vars(config))

    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    dataset = KMRDDataset(config.data_path)

    train_size = int(len(dataset) * config.train_ratio)
    valid_size = int(len(dataset) * config.valid_ratio)
    test_size = len(dataset) - train_size - valid_size
    train_dataset, valid_dataset, test_dataset = (
        torch.utils.data.random_split(
            dataset, (train_size, valid_size, test_size)
        )
    )
    print("Train:", train_size)
    print("Valid:", valid_size)

    train_data_loader = DataLoader(train_dataset, batch_size=config.batch_size)
    valid_data_loader = DataLoader(valid_dataset, batch_size=config.batch_size)

    model = DeepFactorizationMachineModel(
        dataset.user_movie_cnts,
        config.embed_dim,
        config.mlp_dims
    ).to(device)
    optimizer = optim.Adam(params=model.parameters(), lr=0.001, weight_decay=1e-6)
    crit = nn.BCELoss().to(device)

    trainer = Trainer(model, optimizer, crit, device)
    trainer.train(train_data_loader, valid_data_loader, config)

    torch.save(
        {
            'model': trainer.model.state_dict(),
            'config': config
        },
        config.model_fn
    )


if __name__ == '__main__':
    config = define_argparser()
    main(config)



