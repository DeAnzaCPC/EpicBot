import json
import random

ls = []
listCreated = False


class Problem:

    def __init__(self, p_id: str, p_diff: int):
        self.problem_id = p_id
        if p_diff == None:
            self.diff = 9000
        else:
            self.diff = p_diff

    def __lt__(self, other):
        return self.diff < other.diff

    def __eq__(self, other):
        return self.diff == other.diff


def create_list():
    f = open('problem-models.json')
    data = json.load(f)
    for prob in data:
        diff = data[prob].get('difficulty')
        p_id = prob
        p = Problem(p_id, diff)
        ls.append(p)
    ls.sort()
    listCreated = True


def get_problem(rating: int, delta=300) -> str:
    if rating is None:
        rating = 0
    if not listCreated:
        create_list()

    l = 0
    r = len(ls)
    while r - l > 1:
        m = (l + r) // 2
        if ls[m].diff >= (rating - delta):
            r = m
        else:
            l = m

    start = r

    l = 0
    r = len(ls)
    while r - l > 1:
        m = (l + r) // 2
        if ls[m].diff >= (rating + delta):
            r = m
        else:
            l = m

    end = r
    select = random.randint(start, end)
    # print(ls[select].problem_id, ls[select].diff)
    return ls[select].problem_id
