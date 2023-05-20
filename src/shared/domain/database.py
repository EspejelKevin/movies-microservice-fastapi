from contextlib import contextmanager
import abc


class Session:
    pass


class Database:
    @abc.abstractmethod
    @contextmanager
    def session(self): pass