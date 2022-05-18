from abc import ABCMeta, abstractmethod


class BaseOJ(metaclass=ABCMeta):
    @abstractmethod
    def select_problem(self, handle1, handle2):
        pass

    @abstractmethod
    def get_winner(self, handle1, handle2, pid):
        pass

    @abstractmethod
    def get_url(self, pid):
        pass
