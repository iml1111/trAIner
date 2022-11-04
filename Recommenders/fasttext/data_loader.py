import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(verbose=True)

MONGODB_URI = os.getenv('MONGODB_URI')
cli = MongoClient(MONGODB_URI)
db = cli.trainer


def refine_corpora():
    """시퀀스 정제해서 DB에 insert하기"""
    pass



def load_corpora():
    """DB에 있는 정제된 시퀀스 리스트를 단순히 가져옴."""
    pass