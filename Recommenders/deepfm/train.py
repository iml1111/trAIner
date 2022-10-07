import os
import argparse
from pprint import pprint
import torch
from torch import optim
import torch.nn as nn
from dotenv import load_dotenv

"""https://github.com/iml1111/Pytorch-Recommender/blob/main/src/3_DeepFM/train.py"""
load_dotenv(verbose=True)

KMRD_LARGE_DATA_PATH=os.environ['KMRD_LARGE_DATA_PATH']
KMRD_SMALL_DATA_PATH=os.environ['KMRD_SMALL_DATA_PATH']


def define_argparser():
    pass


def main(config):
    pass


if __name__ == '__main__':
    config = define_argparser()
    main(config)



