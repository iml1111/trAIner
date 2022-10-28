import argparse, os
from pprint import pprint
from util import get_movielens, make_sparse_matrix
from util import get_trainer_dataset, make_trainer_matrix
from model import SGD
from dotenv import load_dotenv

load_dotenv(verbose=True)

TRAINER_DATA_PATH_V1=os.getenv('TRAINER_DATA_PATH_V1')
TRAINER_DATA_PATH_V2=os.getenv('TRAINER_DATA_PATH_V2')



def define_argparser():
    p = argparse.ArgumentParser()

    p.add_argument(
        '--k',
        type=int,
        help='latent factor size.'
    )
    p.add_argument(
        '--data_path',
        default=TRAINER_DATA_PATH_V1,
        help='Dataset Path, Default=%(default)s'
    )
    p.add_argument(
        '--n_epochs',
        type=int,
        default=10,
        help='num of Iterations'
    )
    p.add_argument(
        '--lr',
        type=float,
        default=0.01,
        help='learning rate.'
    )
    p.add_argument(
        '--beta',
        type=float,
        default=0.01,
        help='regularization parameter.'
    )
    p.add_argument(
        '--sgd',
        action='store_true',
        help='Use SGD Algorithm.'
    )

    return p.parse_args()


def main(config):
    pprint(vars(config))
    
    #ratings_df = get_movielens('ratings.csv')
    ratings_df = get_trainer_dataset()
    
    print("Rating set shape:", ratings_df.shape)
    
    #sparse_matrix, test_set = make_sparse_matrix(ratings_df)
    sparse_matrix, test_set = make_trainer_matrix(config.data_path)
    
    print("Sparse Matrix shape:", sparse_matrix.shape)
    print("Test set length:", len(test_set))

    if config.sgd:
        trainer = SGD(
            sparse_matrix,
            config.k,
            config.lr,
            config.beta,
            config.n_epochs
        )
    else:
        raise RuntimeError('Algorithm No Selected')

    trainer.train()
    print("train RMSE:", trainer.evaluate())
    print("test RMSE:", trainer.test_evaluate(test_set))


if __name__ == '__main__':
    config = define_argparser()
    main(config)