from bson import ObjectId
from config import config
from . import api_v1 as api
from flask import g, jsonify, current_app
from app.api.response import response_200, bad_request, not_found
from app.api.decorator import timer, login_required
from model.mongodb import User, Problem, SolveLog
from controller.topic_predictor import TopicPredictor
from flask_validation_extended import Json, Validator, Route, Query, Min, Max
from app.api.validation import ObjectIdValid


@api.route('/problems/me', methods=['GET'])
@Validator(bad_request)
@login_required
@timer
def get_my_solve_log(
    skip=Query(int, default=0, rules=Min(0)),
    limit=Query(int, default=10, rules=Min(1))
):
    """내가 푼 문제 반환"""
    user = User(current_app.db).get_userinfo_simple(
        user_oid=g.user_oid
    )
    solve_logs = SolveLog(current_app.db).get_solve_log(
        user_id=user['userId'],
        skip=skip,
        limit=limit
    )
    return response_200(solve_logs)


@api.route('/problems/<problem_id>', methods=['GET'])
@Validator(bad_request)
@login_required
@timer
def get_problem_detail(
    problem_id=Route(str, rules=[ObjectIdValid()])
):
    """단일 문제 반환"""
    problem_oid = ObjectId(problem_id)
    problem = Problem(current_app.db).get_problem_info(
        pro_id=problem_oid
    )
    if not problem:
        return not_found
    return response_200(problem)


@api.route('/problems/curriculum/<problem_id>', methods=['GET'])
@Validator(bad_request)
@login_required
@timer
def get_curriculum(
    problem_id=Route(str, rules=[ObjectIdValid()]),
    count=Query(int, optional=True, rules=[Min(1), Max(20)])
):
    """동적 커리큘럼 목록 반환"""
    problem_oid = ObjectId(problem_id)
    result = Problem(current_app.db).get_problem_number(
        pro_id=problem_oid
    )
    if not result:
        return not_found

    predictor = TopicPredictor(config.TOPIC_MODEL_PATH)
    #Hot Problem이 아닌 경우 not found
    if (
        'problemNumber' not in result.keys() or
        not predictor.is_in_dict(str(result['problemNumber']))
    ):
        return not_found
    
    #문제 반환 개수 default = 10
    #토픽 모델을 통해 가까운 문제들 선별
    items = predictor.get_similar_items(
        str(result['problemNumber']),
        num=count if count else 10
    )
    problem_numbers = [int(i[0]) for i in items]
    problems = Problem(current_app.db).get_problem_info_with_numbers(
        pro_numbers=problem_numbers
    )
    data = []
    for i in items:
        for problem in problems:
            #모델을 통해 얻은 정확도 삽입
            if int(i[0]) == problem['problemNumber']:
                problem['modelAccuracy'] = i[1]
                data.append(problem)
                break    
    return response_200(data)


@api.route('/problems/<problem_id>/submit', methods=['POST'])
@Validator(bad_request)
@login_required
@timer
def submit_problem(
    problem_id=Route(str),
    code=Json(str)
):
    """문제 제출/채점"""
    return response_200()



"""
단일 문제 통계 반환 -> 보류
"""