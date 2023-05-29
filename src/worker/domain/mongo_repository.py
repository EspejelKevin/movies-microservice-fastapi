from abc import ABCMeta, abstractmethod
from typing import List


class MongoRepository(metaclass=ABCMeta):
    @abstractmethod
    def is_up(self) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def create_movie(self, movie: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_movies(self, type_order: int = 1, filters: dict = {}) -> List[dict]:
        raise NotImplementedError

    @abstractmethod
    def get_movie_by_id(self, _id: int) -> dict:
        raise NotImplementedError

    @abstractmethod
    def update_movie(self, _id: int, new_movie: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete_movie(self, _id: int) -> bool:
        raise NotImplementedError
