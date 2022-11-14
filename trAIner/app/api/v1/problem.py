from . import api_v1 as api
from config import config
from flask import g, current_app
from controller.util import make_tier_map
from app.api.response import response_200, bad_request, not_found
from app.api.decorator import timer, login_required
from model.mongodb import User, Problem, SolveLog, Interact
from flask_validation_extended import Json, Validator, Route, Query, Min, Max
from controller.topic_predictor import sort_problems_by_accuracy
from controller.hot_problem import (
    get_similar_problems,
    get_click_problems,
    get_vulnerable_problems,
    get_unfamiliar_problems
)


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
    problem = Problem(current_app.db).get_problem_info(
        pro_id=problem_id
    )
    if not problem:
        return not_found
    return response_200(problem)


@api.route('/problems/curriculum/<problem_id>', methods=['GET'])
@Validator(bad_request)
@login_required
@timer
def get_curriculum(
    problem_id=Route(str),
    count=Query(int, optional=True, rules=[Min(1), Max(20)])
):
    """동적 커리큘럼 목록 반환"""
    result = Problem(current_app.db).get_problem_number(
        pro_id=problem_id
    )
    if not result:
        return not_found

    predictor = current_app.topic_predictor
    #Hot Problem이 아닌 경우 not found
    if (
        'problemNumber' not in result or
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
    data =  sort_problems_by_accuracy(items, problems)
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


@api.route('/problems/hot', methods=['GET'])
@Validator(bad_request)
@login_required
@timer
def get_hot_problems(
    feed=Query(str),
    count=Query(int, default=10, rules=[Min(1), Max(20)])
):
    """핫 유저 문제 반환"""
    if feed == 'similar':
        data = get_similar_problems(current_app.db, g.user_id, count)
    elif feed == 'click':
        data = get_click_problems(current_app.db, g.user_id, count)
    elif feed == 'vulnerable':
        data = get_vulnerable_problems(current_app.db, g.user_id, count)
    elif feed == 'unfamiliar':
        data = get_unfamiliar_problems(current_app.db, g.user_id, count)
    else:
        return bad_request('not supported feed.')
    
    return response_200(data)





"""
밑은 아직 미구현
"""
@api.route('/problems/cold/often_wrong', methods=['GET'])
@Validator(bad_request)
@login_required
@timer
def get_cold_problems(
    feed=Query(str),
    count=Query(int, optional=True, rules=[Min(1), Max(20)])
):
    """콜드 유저 문제 반환"""
    
    if feed == 'often_wrong':
        pass
    elif feed == 'popular':
        pass
    else:
        return bad_request('not supported feed.')



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
    predictor = current_app.deep_predictor

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
