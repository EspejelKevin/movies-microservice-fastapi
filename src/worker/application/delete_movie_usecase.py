from shared.domain import Response, SuccessResponse
from shared.infrastructure import ErrorResponse
from ..domain import MongoRepository
import pathlib
import uuid
import os


class DeleteMovieUseCase:
    def __init__(self, mongo_service: MongoRepository):
        self._mongo_service = mongo_service
        self.transaction_id = str(uuid.uuid4())

    def execute(self, id_movie: int):
        _movie = self._mongo_service.get_movie_by_id(id_movie)
        if _movie is None:
            raise ErrorResponse(
                "Failed to get movie. Cannot verify if the movie exists",
                self.transaction_id,
                500
            )
        if not _movie:
            raise ErrorResponse(
                "Movie does not exist. Try again with different ID",
                self.transaction_id,
                404
            )
        result = self._mongo_service.delete_movie(id_movie)
        if not result:
            raise ErrorResponse(
                "Failed to delete movie. Try again",
                self.transaction_id,
                500
            )
        try:
            path = f"{pathlib.Path(__file__).cwd()}/src/{_movie.get('url', '')}"
            os.remove(path)
        except Exception:
            pass

        return SuccessResponse({"status": "Movie deleted with success"}, 200, self.transaction_id)
