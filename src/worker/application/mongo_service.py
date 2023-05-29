from ..domain import MongoRepository
from typing import List


class MongoService(MongoRepository):
    def __init__(self, mongo_repository: MongoRepository) -> None:
        self.__mongo_repository = mongo_repository

    def is_up(self) -> bool:
        return self.__mongo_repository.is_up()

    def create_movie(self, movie: dict) -> bool:
        return self.__mongo_repository.create_movie(movie)

    def get_movies(self, type_order: int = 1, filters: dict = {}) -> List[dict]:
        return self.__mongo_repository.get_movies(type_order, filters)

    def get_movie_by_id(self, _id: int) -> dict:
        return self.__mongo_repository.get_movie_by_id(_id)

    def update_movie(self, _id: int, new_movie: dict) -> bool:
        return self.__mongo_repository.update_movie(_id, new_movie)

    def delete_movie(self, _id: int) -> bool:
        return self.__mongo_repository.delete_movie(_id)
