"""
유저들이 많이 틀리는 문제
유저들이 많이 푼 문제
Cold_3
시도할 가능성이 높은 문제
"""
from config import config
from . import api_v1 as api
from flask import g, current_app
from random import random, uniform
from collections import defaultdict
from app.api.response import response_200, bad_request, not_found
from app.api.decorator import timer, login_required
from model.mongodb import User, Problem, SolveLog, Interact
from flask_validation_extended import Json, Validator, Route, Query, Min, Max
from controller.ctr_predictor import CTRPredictor
from controller.deep_predictor import DeepPredictor
from controller.util import get_random_index, get_tier, make_tier_map
from controller.topic_predictor import (
    TopicPredictor,
    sort_problems_by_accuracy
)


@api.route('/problems/cold/often_wrong', methods=['GET'])
@Validator(bad_request)
@login_required
@timer
def get_often_wrong_problems(
    count=Query(int, optional=True, rules=[Min(1), Max(20)])
):
    """핫 유저들이 많이 틀리는 문제 반환"""
    
    """
    핫 유저에 대하여 각 난이도별로 취약점 평균 수치가 높은 문제를 집단으로 수집하여
    집단에서 일정 부분 랜덤으로 발췌하여 추천 진행
    """
    tiers = config.AVAILABLE_TIER
    result = {}
    for i in tiers:
        result[i] = None
    for tier in tiers:
        result[tier] = Problem(current_app.db).get_problem_number_by_tier(
            tier=tier
        )

    #TODO: 이 부분은 연산량이 많아서 성능저하가 우려됨.. 캐싱?
    #핫 유저
    users = User(current_app.db).get_all_users()
    #취약점 모델
    predictor = DeepPredictor(config.DEEP_MODEL_PATH)

    #난이도별로 모든 핫 유저에 대하여 취약점 계산
    for tier in tiers:
        for user in users:
            vulnerable = []
            problems = result[tier]
            for p in problems:
                vulnerable.append(
                    predictor.predict(user['userNumber'], p['problemNumber'])
                )
            

    return response_200()


@api.route('/problems/cold/popular', methods=['GET'])
@Validator(bad_request)
@login_required
@timer
def get_popular_problems(
    count=Query(int, optional=True, rules=[Min(1), Max(20)])
):
    """유저들이 많이 푼 문제 반환"""

    """많이 해결한건지, 아니면 많이 시도한건지를 정확히 해야할듯"""
    tiers, result = make_tier_map()
    
    # for tier in tiers:
    #     result[tier] = Problem(current_app.db).get_problem_number_by_tier(
    #         tier=tier
    #     )
    
    problems = Problem(current_app.db).get_all_problems()
    

    #핫 유저가 푼 핫 문제 interact 전체
    interact = Interact(current_app.db).get_all_interact()

    for tier in tiers:
        problems = result[tier]
        

            


    return response_200()
