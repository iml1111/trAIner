from random import uniform
from flask import g, current_app
from controller.util import get_random_index
from model.mongodb import User, Problem, SolveLog
from controller.topic_predictor import sort_problems_by_accuracy


def get_similar_problems(count: int):
    """최근에 푼 유형과 비슷한 문제 반환"""
    user = User(current_app.db).get_userinfo_simple(
        user_oid=g.user_oid
    )
    latest_problems = SolveLog(current_app.db).get_solve_log(
        user_id=user['userId'],
        skip=0,
        limit=5
    )
    problem_ids = [i['problemId'] for i in latest_problems]
    result = Problem(current_app.db).get_problem_number_many(
        pro_ids=problem_ids
    )
    predictor = current_app.topic_predictor
    problem_numbers = []
    for i in result:
        #hot problem인 경우에만 모델에 삽입
        if (
            'problemNumber' in i.keys() and
            predictor.is_in_dict(str(i['problemNumber']))
        ):
            problem_numbers.append(str(i['problemNumber']))
    #토픽 모델을 통해 가까운 문제들 선별
    items = predictor.get_similar_items(
        problem_numbers,
        num=count if count else 10
    )
    problem_numbers = [int(i[0]) for i in items]
    problems = Problem(current_app.db).get_problem_info_with_numbers(
        pro_numbers=problem_numbers
    )
    data = sort_problems_by_accuracy(items, problems)
    return data


def get_click_problems(count: int):
    """시도할 가능성이 높은 문제 반환"""
    user = User(current_app.db).get_userinfo_simple(
        user_oid=g.user_oid
    )
    problems = Problem(current_app.db).get_all_problems()
    predictor = current_app.ctr_predictor

    items = []
    for i in problems:
        rate = predictor.predict_probe(user['userNumber'], i['problemNumber'])
        rate = rate + uniform(0, 0.5)  #희재형한테 random값 피드백 받기
        items.append((i['problemNumber'], rate))
    #rate 높은 순으로 정렬
    items = sorted(items, key=lambda x: x[1], reverse=True)

    problem_numbers = []
    #상위 50개의 item중에서 랜덤으로 count만큼 뽑기
    index = get_random_index(
        length=50,
        count=count if count else 10
    )
    for i in index:
        problem_numbers.append(items[i][0])

    data = Problem(current_app.db).get_problem_info_with_numbers(
        pro_numbers=problem_numbers
    )
    return data


def get_vulnerable_problems(count: int):
    """틑릴 가능성이 높은 문제 반환"""


def get_unfamiliar_problems(count: int):
    """익숙하지 않은 유형의 문제 반환"""
    user = User(current_app.db).get_userinfo_simple(
        user_oid=g.user_oid
    )
    problems = Problem(current_app.db).get_all_problems()
    ctr_predictor = current_app.ctr_predictor

    #모든 핫문제에 대한 클릭률 구하기
    items = []
    for i in problems:
        rate = ctr_predictor.predict_probe(user['userNumber'], i['problemNumber'])
        items.append((i['problemNumber'], rate))
    #rate 낮은 순으로 정렬
    items = sorted(items, key=lambda x: x[1])

    #하위 50개의 item중에서 랜덤으로 1개 뽑기
    index = get_random_index(
        length=50,
        count=1
    )
    problem_number = str(items[index[0]][0])

    #토픽모델을 통해 비슷한 문제 선별
    topic_predictor = current_app.topic_predictor
    items = topic_predictor.get_similar_items(
        problem_number,
        num=count if count else 10
    )
    problem_numbers = [int(i[0]) for i in items]
    problems = Problem(current_app.db).get_problem_info_with_numbers(
        pro_numbers=problem_numbers
    )
    data = sort_problems_by_accuracy(items, problems)
    return data