from ..domain import MongoRepository
from typing import Any


class MongoService(MongoRepository):
    def __init__(self, mongo_repository: MongoRepository) -> None:
        self.__mongo_repository = mongo_repository

    def create_movie(self, movie: dict) -> bool:
        return self.__mongo_repository.create_movie(movie)

    def get_movies(self) -> list[dict]:
        return self.__mongo_repository.get_movies()

    def get_movie_by_id(self, _id: int) -> dict:
        return self.__mongo_repository.get_movie_by_id(_id)

    def get_movies_by_filter(self, _filter: Any) -> list[dict] | None:
        return self.__mongo_repository.get_movies_by_filter(_filter)

    def update_movie(self, _id: int, new_movie: dict) -> bool:
        return self.__mongo_repository.update_movie(_id, new_movie)

    def delete_movie(self, _id: int) -> bool:
        return self.__mongo_repository.delete_movie(_id)
