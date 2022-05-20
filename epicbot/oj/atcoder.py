from .base import BaseOJ, Submission
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
import random
import json

ATCODER_SUBMISSION_URL = "https://atcoder.jp/contests/{}/submissions?f.Task={}&f.LanguageName=&f.Status=&f.User={}"
ATCODER_MAX_RATING = 200


class AtcoderOJ(BaseOJ):
    def __init__(self):
        self.problems = []
        self.pid_to_idx = {}
        self._fetch_problems()

    def get_problem(self, rating: int, delta: int) -> str:
        l = -1
        r = len(self.problems) - 1
        while r - l > 1:
            m = (l + r) // 2
            if self.problems[m]['difficulty'] >= (rating - delta):
                r = m
            else:
                l = m

        start = r

        l = -1
        r = len(self.problems) - 1
        while r - l > 1:
            m = (l + r) // 2
            if self.problems[m]['difficulty'] >= (rating + delta):
                r = m
            else:
                l = m

        end = r
        select = random.randint(start, end)
        return self.problems[select]['id']

    def select_problem(self, handle1, handle2):
        return self.get_problem(0, 300)

    def get_url(self, pid):
        return self.problems[self.pid_to_idx[pid]]['url']

    def _fetch_problems(self):
        data = json.load(open('problem-models.json'))
        parsed = []
        pid_to_idx = {}

        def parse_contest_from_id(p_id):
            return re.findall(r'(.*)_+', p_id)[0]

        for id, problem in data.items():
            if 'difficulty' in problem:
                res = {}
                res['difficulty'] = problem['difficulty']
                res['id'] = id
                contest = parse_contest_from_id(id).replace('_', '-')
                res['contest'] = contest
                res['url'] = 'https://atcoder.jp/contests/{}/tasks/{}'.format(
                    contest, id)
                pid_to_idx[id] = len(parsed)
                parsed.append(res)

        self.problems = parsed
        self.pid_to_idx = pid_to_idx
        self.problems.sort(key=lambda p: p['difficulty'])

    def fetch_submissions(self, handle, pid):
        res = []

        idx = self.pid_to_idx[pid]
        problem = self.problems[idx]
        url = ATCODER_SUBMISSION_URL.format(
            problem['contest'], problem['id'], handle)
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        selected = soup.select('.table tr')
        for item in selected[1:]:
            cell = item.select('td')
            if len(cell) == 10:
                date = datetime.strptime(cell[0].text, '%Y-%m-%d %H:%M:%S%z')
                ts = date.timestamp()
                is_ac = cell[6].text == 'AC'
                url = 'https://atcoder.jp' + cell[9].select_one('a').attrs['href']
                res.append(Submission(int(ts), is_ac, url))
        return res
