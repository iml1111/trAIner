tag_map = {
    'implementation': '구현',
    'arithmetic': '사칙연산',
    'math': '수학',
    'number_theory': '정수론',
    'dp': '다이나믹 프로그래밍',
    'data_structures': '자료 구조',
    'graph_theory': '그래프 이론',
    'string': '문자열',
    'greedy': '그리디 알고리즘',
    'bruteforcing': '브루트포스 알고리즘',
    'graph_traversal': '그래프 탐색',
    'sorting': '정렬',
    'trees': '트리',
    'binary_search': '이분 탐색',
    'bfs': '너비 우선 탐색',
    'dfs': '깊이 우선 탐색'
}


def get_tag_name(tags: list):
    data = []
    for tag in tags:
        if tag['key'] in tag_map:
            data.append(tag_map[tag['key']])
        else:
            data.append(tag['key'])
    return data
