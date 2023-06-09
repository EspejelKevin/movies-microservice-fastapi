from ..domain import MongoRepository, MovieModelIn, MovieModel
from shared.domain import Response, SuccessResponse
from shared.infrastructure import ErrorResponse
import uuid


class UpdateMovieUseCase:
    def __init__(self, mongo_service: MongoRepository):
        self._mongo_service = mongo_service
        self.transaction_id = str(uuid.uuid4())

    def execute(self, id_movie: int, movie: MovieModelIn):
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
        movie = MovieModel(**movie, id_movie=id_movie, url=_movie.get("url", ""))
        movie.release_date = str(movie.release_date)
        result = self._mongo_service.update_movie(id_movie, movie.dict())
        if not result:
            raise ErrorResponse(
                "Failed to update movie. Try again",
                self.transaction_id,
                500
            )

        return SuccessResponse({"status": "Movie updated with success"}, 200, self.transaction_id)
