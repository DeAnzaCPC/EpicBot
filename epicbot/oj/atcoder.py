from .base import BaseOJ
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
from random import randint

ATCODER_PROBLEM_LIST_URL = "https://kenkoooo.com/atcoder/resources/problem-models.json"
ATCODER_SUBMISSION_URL = "https://atcoder.jp/contests/{}/submissions?f.Task={}&f.LanguageName=&f.Status=AC&f.User={}"
ATCODER_MAX_RATING = 200

class AtcodeOJ(BaseOJ):
  def __init__(self):
    self.problems = []
    self.pid_to_idx = {}
    self._fetch_problems()

  def select_problem(self, handle1, handle2):
    filtered = [p for p in self.problems if p['difficulty'] < ATCODER_MAX_RATING]
    return filtered[randint(0, len(filtered)-1)]['id']

  def get_winner(self, handle1, handle2, pid):
    inf = 1e18
    time1 = self._fetch_submission_time(handle1, pid)
    time2 = self._fetch_submission_time(handle2, pid)
    if time1 is None:
      time1 = inf
    if time2 is None:
      time2 = inf
    if time1 < time2:
      return handle1
    if time2 < time1:
      return handle2
    if time1 == inf and time2 == inf:
      return None
    return [handle1, handle2][randint(0,1)] # random roulette the draw lol

  def get_url(self, pid):
    return self.problems[self.pid_to_idx[pid]]['url']

  def _fetch_problems(self):
    req = requests.get(ATCODER_PROBLEM_LIST_URL)
    req_json = req.json()
    parsed = []
    pid_to_idx = {}

    def parse_contet_from_id(id):
      return re.findall(r'(.*?)_[^_]+', id)[0]

    for id, problem in req_json.items():
      if 'difficulty' in problem:
        res = {}
        res['difficulty'] = problem['difficulty']
        res['id'] = id
        contest = parse_contet_from_id(id)
        res['contest'] = contest
        res['url'] = 'https://atcoder.jp/contests/{}/tasks/{}'.format(contest, id)
        pid_to_idx[id] = len(parsed)
        parsed.append(res)
    
    self.problems = parsed
    self.pid_to_idx = pid_to_idx
  
  def _fetch_submission_time(self, handle, pid):
    res = None

    idx = self.pid_to_idx[pid]
    problem = self.problems[idx]
    url = ATCODER_SUBMISSION_URL.format(problem['contest'], problem['id'], handle)
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    selected = soup.select('.table tr')
    for item in selected:
      cell = item.select_one('.fixtime-second')
      if cell is not None:
        date = datetime.strptime(cell.text, '%Y-%m-%d %H:%M:%S%z')
        ts = date.timestamp()
        if res is None:
          res = ts
        else:
          res = min(res, ts)
    
    if res is not None:
      return int(res)
    else:
      return None
