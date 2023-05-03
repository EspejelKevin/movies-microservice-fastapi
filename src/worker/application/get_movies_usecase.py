from shared.domain import Response, SuccessResponse
from shared.infrastructure import ErrorResponse
from ..domain import MongoRepository, QueryFilterModel
import uuid


class GetMoviesUseCase:
    def __init__(self, mongo_service: MongoRepository):
        self._mongo_service = mongo_service
        self.transaction_id = str(uuid.uuid4())

    def execute(self, query_params: QueryFilterModel):
        movies = self._mongo_service.get_movies()
        if movies is None:
            raise ErrorResponse(
                "Failed to get movies. Try again",
                self.transaction_id,
                500
            )
        return SuccessResponse(list(movies), 200, self.transaction_id)
