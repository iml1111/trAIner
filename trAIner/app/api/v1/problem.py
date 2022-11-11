from bson import ObjectId
from . import api_v1 as api
from flask import g, jsonify, current_app
from app.api.response import response_200, bad_request
from app.api.decorator import timer, login_required
from model.mongodb import User, Problem, SolveLog
from flask_validation_extended import Json, Validator, Route, Query, Min


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
    problem_id=Route(str)
):
    """단일 문제 반환"""
    problem_oid = ObjectId(problem_id)
    problem = Problem(current_app.db).get_problem_info(
        pro_id=problem_oid
    )
    return response_200(problem)


@api.route('/problems/curriculum', methods=['GET'])
@Validator(bad_request)
@login_required
@timer
def get_curriculum(
    problem_id=Route(str),
    code=Json(str)
):
    """개인 동적 커리큘럼 목록 반환"""
    return response_200()


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