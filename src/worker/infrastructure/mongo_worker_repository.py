from shared.infrastructure import get_settings
from ..domain import MongoRepository
from typing import Any


settings = get_settings()


class MongoWorkerRepository(MongoRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def create_movie(self, movie: dict) -> bool:
        with self.session_factory() as session:
            db = session.get_db(settings.MONGO_DB_NAME)
            collection = db.movies
            result = collection.insert_one(movie)
            return result.inserted_id is not None

    def get_movies(self) -> list[dict]:
        with self.session_factory() as session:
            db = session.get_db(settings.MONGO_DB_NAME)
            collection = db.movies
            result = collection.find(projection={"_id": False})
            return result

    def get_movie_by_id(self, _id: int) -> dict:
        with self.session_factory() as session:
            db = session.get_db(settings.MONGO_DB_NAME)
            collection = db.movies
            result = collection.find_one(
                {"id_movie": _id},
                projection={"_id": False}
            )
            return result

    def update_movie(self, _id: int, new_movie: dict) -> bool:
        with self.session_factory() as session:
            db = session.get_db(settings.MONGO_DB_NAME)
            collection = db.movies
            result = collection.replace_one({"id_movie": _id}, new_movie)
            return result.modified_count > 0

    def delete_movie(self, _id: int) -> bool:
        with self.session_factory() as session:
            db = session.get_db(settings.MONGO_DB_NAME)
            collection = db.movies
            result = collection.delete_one({"id_movie": _id})
            return result.deleted_count > 0

    def get_movies_by_filter(self, _filter: Any) -> list[dict] | None:
        pass
