from flask import g, current_app
from controller.util import get_random_index
from model.mongodb import Problem, MasterConfig
from controller.topic_predictor import sort_problems_by_accuracy
from pymongo import MongoClient

#기본적으로 콜드 스타트 유저들은 데이터가 부족하므로 핫 유저들의 데이터를 토대로 추천 진행

def get_cold_vulnerable_problems(db: MongoClient, count: int):
    """유저들이 많이 틀리는 문제 반환"""
    vulnerable = MasterConfig(db).get_vulnerable()
    result = vulnerable['value']

    problem_ids = []
    for tier, value in result.items():
        index = get_random_index(
            length=len(value),
            count=4
        )
        for i in index:
            problem_ids.append(value[i])
    
    data = Problem(db).get_problem_info_many(
        pro_ids=problem_ids
    )
    return data


def get_cold_click_problems(db: MongoClient, count: int):
    """시도할 가능성이 높은 문제 반환"""
    click = MasterConfig(db).get_click()
    result = click['value']

    problem_ids = []
    for tier, value in result.items():
        index = get_random_index(
            length=len(value),
            count=4
        )
        for i in index:
            problem_ids.append(value[i])
    
    data = Problem(db).get_problem_info_many(
        pro_ids=problem_ids
    )
    return data
    

def get_cold_popular_problems(db: MongoClient, count: int):
    """유저들이 많이 푼 문제 반환"""
    popular = MasterConfig(db).get_popular()
    result = popular['value']

    problem_ids = []
    for tier, value in result.items():
        index = get_random_index(
            length=len(value),
            count=4
        )
        for i in index:
            problem_ids.append(value[i])
    
    data = Problem(db).get_problem_info_many(
        pro_ids=problem_ids
    )
    return data


def get_cold_algorithm_problems(db: MongoClient, content: str, count: int):
    """알고리즘별 문제 반환"""
    algorithm = MasterConfig(db).get_algorithm()
    result = algorithm['value']

    problem_ids = result[content]
    #interact가 가장 많은 문제를 토픽모델에 넣음
    problem = Problem(db).get_problem_number(
        pro_id=problem_ids[0]
    )

    topic_predictor = current_app.topic_predictor
    items = topic_predictor.get_similar_items(
        str(problem['problemNumber']),
        num=count
    )
    problem_numbers = [int(i[0]) for i in items]
    problems = Problem(db).get_problem_info_with_numbers(
        pro_numbers=problem_numbers
    )
    data = sort_problems_by_accuracy(items, problems)
    return data