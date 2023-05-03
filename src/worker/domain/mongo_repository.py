from abc import ABCMeta, abstractmethod
from typing import Any


class MongoRepository(metaclass=ABCMeta):
    @abstractmethod
    def create_movie(self, movie: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_movies(self) -> list[dict]:
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

    @abstractmethod
    def get_movies_by_filter(self, _filter: Any) -> list[dict] | None:
        raise NotImplementedError
