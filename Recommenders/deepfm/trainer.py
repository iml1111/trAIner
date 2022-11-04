from copy import deepcopy
import torch
from tqdm import tqdm
import numpy as np


class Trainer:

    def __init__(self, model, optim, crit, device):
        self.model = model
        self.optim = optim
        self.crit = crit
        self.device = device

    def _train(self, data_loader, config):
        """1 Epoch Train"""
        self.model.train()
        total_loss = 0
        batches = tqdm(
            data_loader,
            desc="train:nan | p:nan | g:nan",
            leave=False
        )

        for x, y in batches:
            x, y = x.to(self.device), y.to(self.device)
            y_hat = self.model(x)
            loss = self.crit(y_hat, y)

            self.optim.zero_grad()
            loss.backward()
            self.optim.step()

            batches.set_description(
                "train:%.4e | p:%.4e | g:%.4e" % (
                    float(loss),
                    float(
                        self.get_parameter_norm(
                            self.model.parameters()
                        )
                    ),
                    float(
                        self.get_grad_norm(
                            self.model.parameters()
                        )
                    ),
                )
            )
            batches.refresh()
            total_loss += float(loss)

        return total_loss / len(data_loader)

    def _valid(self, data_loader, config):
        self.model.eval()
        total_loss = 0

        with torch.no_grad():
            batches = tqdm(
                data_loader,
                desc="valid:nan | p:nan | g:nan",
                leave=False
            )
            for x, y in batches:
                x, y = x.to(self.device), y.to(self.device)
                y_hat = self.model(x)
                loss = self.crit(y_hat, y)

                batches.set_description(
                    "valid:%.4e | p:%.4e | g:%.4e" % (
                        float(loss),
                        float(
                            self.get_parameter_norm(
                                self.model.parameters()
                            )
                        ),
                        float(
                            self.get_grad_norm(
                                self.model.parameters()
                            )
                        ),
                    )
                )
                batches.refresh()
                total_loss += float(loss)

        return total_loss / len(data_loader)

    def train(
            self,
            train_data_loader,
            valid_train_loader,
            config
    ):
        lowest_loss = np.inf
        best_model = None

        for epoch in range(config.n_epochs):
            train_loss = self._train(train_data_loader, config)
            valid_loss = self._valid(valid_train_loader, config)

            if valid_loss <= lowest_loss:
                lowest_loss = valid_loss
                best_model = deepcopy(self.model.state_dict())

            print("Epoch(%d/%d): train_loss=%.4e valid_loss=%.4e lowest_loss=%.4e" % (
                epoch + 1,
                config.n_epochs,
                train_loss,
                valid_loss,
                lowest_loss,
            ))

        self.model.load_state_dict(best_model)

    @staticmethod
    def get_grad_norm(parameters, norm_type=2):
        parameters = list(filter(lambda p: p.grad is not None, parameters))
        total_norm = 0

        for p in parameters:
            param_norm = p.grad.data.norm(norm_type)
            total_norm += param_norm ** norm_type
        total_norm = total_norm ** (1. / norm_type)

        return total_norm

    @staticmethod
    def get_parameter_norm(parameters, norm_type=2):
        total_norm = 0

        for p in parameters:
            param_norm = p.data.norm(norm_type)
            total_norm += param_norm ** norm_type
        total_norm = total_norm ** (1. / norm_type)

        return total_norm
