from shared.domain import Response, SuccessResponse
from shared.infrastructure import ErrorResponse
from ..domain import MongoRepository
import uuid


class DeleteMovieUseCase:
    def __init__(self, mongo_service: MongoRepository):
        self._mongo_service = mongo_service
        self.transaction_id = str(uuid.uuid4())

    def execute(self, id_movie: int):
        _movie = self._mongo_service.get_movie_by_id(id_movie)
        if _movie is None:
            raise ErrorResponse(
                "Movie does not exist. Try again",
                self.transaction_id,
                500
            )
        result = self._mongo_service.delete_movie(id_movie)
        if result is None:
            raise ErrorResponse(
                "Failed to delete movie. Try again",
                self.transaction_id,
                500
            )

        return SuccessResponse({"status": "Movie deleted with success"}, 200, self.transaction_id)
