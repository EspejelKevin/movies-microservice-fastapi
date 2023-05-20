from shared.domain import Response, SuccessResponse
from shared.infrastructure import ErrorResponse
from ..domain import MongoRepository, QueryFilterModel
import uuid


class GetMoviesUseCase:
    def __init__(self, mongo_service: MongoRepository):
        self._mongo_service = mongo_service
        self.transaction_id = str(uuid.uuid4())

    def execute(self, query_params: QueryFilterModel):
        filters = query_params.dict(exclude_none=True)
        type_order = -1 if filters.pop("release_date_desc") else 1
        movies = self._mongo_service.get_movies(type_order, filters)
        if movies is None:
            raise ErrorResponse(
                "Failed to get movies. Try again",
                self.transaction_id,
                500
            )
        return SuccessResponse(list(movies), 200, self.transaction_id)
