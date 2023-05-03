from shared.domain import Response, SuccessResponse
from shared.infrastructure import ErrorResponse
from ..domain import MongoRepository
import uuid


class GetMovieUseCase:
    def __init__(self, mongo_service: MongoRepository):
        self._mongo_service = mongo_service
        self.transaction_id = str(uuid.uuid4())

    def execute(self, id_movie: int):
        movie = self._mongo_service.get_movie_by_id(id_movie)
        if movie is None:
            raise ErrorResponse(
                "Failed to get movie. Try again",
                self.transaction_id,
                500
            )
        return SuccessResponse(movie, 200, self.transaction_id)
