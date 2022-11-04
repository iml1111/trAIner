import os
import json
from collections import defaultdict
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(verbose=True)

MONGODB_URI = os.getenv('MONGODB_URI')
cli = MongoClient(MONGODB_URI)
db = cli['trainer_recom']

DATA_PATH = os.getenv('DATA_PATH')


def refine_corpora_v1():
    """시퀀스 정제해서 DB에 insert하기"""
    with open(DATA_PATH, 'r') as f:
        interacts = json.load(f)
    print("# 총 인터렉션 수:", len(interacts))
    
    # db['hot_interacts'].drop()
    # db['hot_interacts'].insert_many(interacts)
    # print("# 인터렉션 삽입 완료.")
    
    for i in interacts:
        i['userId'] = str(i['userId'])
        i['problemId'] = str(i['problemId'])
        i['timestamp'] = int(i['timestamp'])
    interacts.sort(key=lambda x: x['timestamp'])

    user_dict = defaultdict(lambda: {'sequence':[]})
    for i in interacts:
        if (
            len(user_dict[i['userId']]['sequence']) >= 2
            and (
                user_dict[i['userId']]['sequence'][-1] == i['problemId']
                or user_dict[i['userId']]['sequence'][-2] == i['problemId']
            )
        ) or (
            len(user_dict[i['userId']]['sequence']) >= 1
            and user_dict[i['userId']]['sequence'][-1] == i['problemId']
        ):
            pass
        else:
            user_dict[i['userId']]['sequence'].append(i['problemId'])

    user_seq_docs = []
    for user_id in user_dict:
        value = user_dict[user_id]
        sequence = value['sequence']
        user_seq_docs.append({
            'user_id': user_id,
            'sequence': sequence,
        })

    db['sequence'].insert_many(user_seq_docs)



def load_corpora():
    """DB에 있는 정제된 시퀀스 리스트를 단순히 가져옴."""
    sequences = list(db['sequence'].find({}, {'_id': 0, 'sequence': 1}))
    sequences = [i['sequence'] for i in sequences]
    return sequences


if __name__ == '__main__':
    #refine_corpora_v1()
    
    from pprint import pprint
    sequences = load_corpora()
    pprint(sequences[:2])
