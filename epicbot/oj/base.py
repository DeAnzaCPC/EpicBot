from abc import ABCMeta, abstractmethod
from collections import namedtuple

Submission = namedtuple('Submission', ['timestamp', 'is_ac', 'url'])

class BaseOJ(metaclass=ABCMeta):
    @abstractmethod
    def select_problem(self, handle1, handle2):
        pass

    @abstractmethod
    def fetch_submissions(self, handle, pid):
        pass

    @abstractmethod
    def get_url(self, pid):
        pass
