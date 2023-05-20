from shared.domain import Response, SuccessResponse
from shared.infrastructure import ErrorResponse
from worker.domain import MongoRepository
import uuid


class ReadinessUseCase:
    def __init__(self, mongo_service: MongoRepository) -> None:
        self._mongo_service = mongo_service
        self.transaction_id = str(uuid.uuid4())
    
    def execute(self) -> Response:
        if not self._mongo_service.is_up():
            raise ErrorResponse(
                "Mongo connection error",
                self.transaction_id,
                500
            )
        
        return SuccessResponse({"status": "Mongo is up"}, 200, self.transaction_id)