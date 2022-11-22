from . import api_v1 as api
from config import config
from flask import g, current_app
from app.api.response import response_200, bad_request, not_found
from app.api.decorator import timer, login_required
from model.mongodb import User, Problem, SolveLog
from flask_validation_extended import Json, Validator, Route, Query, Min, Max
from controller.topic_predictor import sort_problems_by_accuracy
from controller.python_executor import run_problem
from controller.tag import get_tag_name, tag_map
from controller.hot_problem import (
    get_hot_similar_problems,
    get_hot_click_problems,
    get_hot_vulnerable_problems,
    get_hot_unfamiliar_problems
)
from controller.cold_problem import (
    get_cold_vulnerable_problems,
    get_cold_popular_problems,
    get_cold_algorithm_problems,
    get_cold_click_problems
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
    for p in solve_logs:
        p['tags'] = get_tag_name(p['tags'])
    return response_200(solve_logs)


@api.route('/problems/me/latest', methods=['GET'])
@Validator(bad_request)
@login_required
@timer
def get_my_latest_solve_log():
    """내가 가장 최근에 맞춘 문제 반환"""
    s = SolveLog(current_app.db).get_latest_solve_log(
        user_id=g.user_id,
    )
    if not s:
        return not_found
    s = s[0]
    p = Problem(current_app.db).get_problem_info(
        pro_id=s['problemId']
    )
    if not p:
        return not_found

    tags = get_tag_name(p['tags'])

    return response_200({
    'userId': s['userId'],
    'problemId': s['problemId'],
    'result': s['result'],
    'executionTime': s['executionTime'],
    'code': s['code'],
    'titleKo': p['titleKo'],
    'level': p['level'],
    'tags': tags,
    'correctPeople': p['correctPeople'],
    'timeLimit': p['timeLimit'],
    'memoryLimit': p['memoryLimit'],
    'description': p['description'],
    'input': p['input'],
    'output': p['output'],
    'example': p['example'],
    'limit': p['limit'],
    'note': p['note'],
    'created_at': s['created_at']
})


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

    #최근에 푼 기록이 있으면 코드 삽입
    problem['code'] = None
    solve_log = SolveLog(current_app.db).get_latest_solve_log_by_problem_id(
        user_id=g.user_id,
        pro_id=problem_id
    )
    if solve_log:
        problem['code'] = solve_log[0]['code']

    problem['tags'] = get_tag_name(problem['tags'])
    return response_200(problem)


@api.route('/problems/curriculum/<problem_id>', methods=['GET'])
@Validator(bad_request)
@login_required
@timer
def get_curriculum(
    problem_id=Route(str),
    count=Query(int, default=30, rules=Min(1))
):
    """동적 커리큘럼 목록 반환"""
    result = Problem(current_app.db).get_problem_number(
        pro_id=problem_id
    )
    if not result:
        return not_found

    predictor = current_app.topic_predictor
    # Hot Problem이 아닌 경우 not found
    if (
        'problemNumber' not in result or
        not predictor.is_in_dict(str(result['problemNumber']))
    ):
        return not_found
    
    # 문제 반환 개수 default = 10
    # 토픽 모델을 통해 가까운 문제들 선별
    items = predictor.get_similar_items(
        str(result['problemNumber']),
        num=count
    )
    problem_numbers = [int(i[0]) for i in items]
    problems = Problem(current_app.db).get_problem_info_with_numbers(
        pro_numbers=problem_numbers
    )
    #태그 이름 변환
    for p in problems:
        p['tags'] = get_tag_name(p['tags'])

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
    problem = Problem(current_app.db).get_problem_info(
        pro_id=problem_id
    )
    if not problem:
        return not_found
    
    input = problem['example'][0]['sample_input']
    output = problem['example'][0]['sample_output']
    
    result = run_problem(code, input, output)

    SolveLog(current_app.db).insert_solve_log({
        'userId': g.user_id,
        'problemId': problem_id,
        'result': result['result'],
        'description': result['description'],
        'executionTime': result['time'],
        'code': code,
        'problemNumber': problem['problemNumber']
    })
    
    if result:
        latest = SolveLog(current_app.db).get_latest_solve_log(
            user_id=g.user_id
        )
        #맞춘 기록이 없을 경우, 문제 맞춘 인원 업데이트
        if not latest:
            Problem(current_app.db).update_problem(
                pro_id=problem_id,
                document={
                    'correctPeople': problem['correctPeople'] + 1
                }
            )
            user = User(current_app.db).get_userinfo(
                user_oid=g.user_oid
            )
            #유저의 맞춘 문제 개수 갱신 및 cold -> hot으로 변경
            User(current_app.db).update_user(
                user_oid=g.user_oid,
                document={
                    'count': user['count'] + 1,
                    'isHotUser': True if user['count'] + 1 >= 10 else user['isHotUser']
                }
            )
    return response_200(result)


"""
단일 문제 통계 반환 -> 보류
"""


@api.route('/problems/hot', methods=['GET'])
@Validator(bad_request)
@login_required
@timer
def get_hot_problems(
    feed=Query(str),
    count=Query(int, default=30, rules=Min(1))
):
    """핫 유저 문제 반환"""
    user = User(current_app.db).get_userinfo_simple(
        user_oid=g.user_oid
    )
    #핫 유저가 아닌 경우 400
    if not user['isHotUser']:
        return bad_request('You are not hot user.')

    if feed == 'similar':
        data = get_hot_similar_problems(current_app.db, g.user_id, count)
    elif feed == 'click':
        data = get_hot_click_problems(current_app.db, g.user_id, count)
    elif feed == 'vulnerable':
        data = get_hot_vulnerable_problems(current_app.db, g.user_id, count)
    elif feed == 'unfamiliar':
        data = get_hot_unfamiliar_problems(current_app.db, g.user_id, count)
    else:
        return bad_request('not supported feed.')
    #태그 이름 변환
    for p in data:
        p['tags'] = get_tag_name(p['tags'])

    return response_200(data)


@api.route('/problems/cold', methods=['GET'])
@Validator(bad_request)
@login_required
@timer
def get_cold_problems(
    feed=Query(str),
    content=Query(str, optional=True, rules=[]),
    count=Query(int, default=10, rules=[Min(1), Max(20)])
):
    """콜드 유저 문제 반환"""
    user = User(current_app.db).get_userinfo_simple(
        user_oid=g.user_oid
    )
    #콜드 유저가 아닌 경우 400
    if user['isHotUser']:
        return bad_request('You are not cold user.')

    if feed == 'vulnerable':
        data = get_cold_vulnerable_problems(current_app.db, count)
    elif feed == 'popular':
        data = get_cold_popular_problems(current_app.db, count)
    elif feed == 'click':
        data = get_cold_click_problems(current_app.db, count)
    elif feed == 'algorithm':
        if not content:
            return bad_request('content is needed.')
        if content not in tag_map:
            return  bad_request('content is not supported.')
        data = get_cold_algorithm_problems(current_app.db, content, count)
    else:
        return bad_request('not supported feed.')

    #태그 이름 변환
    for p in data:
        p['tags'] = get_tag_name(p['tags'])
    
    return response_200(data)