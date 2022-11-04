import os
import numpy as np
import pandas as pd


def get_trainer_dataset(data_path):
    df = pd.read_csv(data_path, encoding='utf-8')
    return df.sample(frac=1).reset_index(drop=True)


def make_trainer_matrix(df):
    """
    Make sparse matrix
    :param df: train_df [userId, movieId, rating, ...]
    :return: sparse_matrix (movie_n) * (user_n)
    """
    sparse_matrix = (
        df
        .groupby('problemId')
        .apply(lambda x: pd.Series(x['value'].values, index=x['userId']))
        .unstack()
    )
    sparse_matrix.index.name = 'problemId'

    test_set = [] # (movie_id, user_id, rating)
    idx, jdx = sparse_matrix.fillna(0).to_numpy().nonzero()
    indice = list(zip(idx, jdx))
    np.random.shuffle(indice)

    for i, j in indice[:df.shape[0] // 9]:
        test_set.append((i, j, sparse_matrix.iloc[i, j]))
        sparse_matrix.iloc[i, j] = 0

    return sparse_matrix, test_set
