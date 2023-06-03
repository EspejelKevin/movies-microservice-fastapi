from ..domain import MongoRepository, MovieModelIn, MovieModel
from shared.domain import Response, SuccessResponse
from shared.infrastructure import ErrorResponse
import uuid


class CreateMovieUseCase:
    def __init__(self, mongo_service: MongoRepository):
        self._mongo_service = mongo_service
        self.transaction_id = str(uuid.uuid4())

    def execute(self, movie: MovieModelIn, url: str):
        movies = self._mongo_service.get_movies()
        if movies is None:
            raise ErrorResponse(
                "Failed to get movies. A connection error occurred. Try again",
                self.transaction_id,
                500
            )
        movies = sorted(list(movies), key=lambda m: m.get("id_movie"))
        id_movie = 1
        if movies:
            id_movie = movies[-1].get("id_movie") + 1
        movie = MovieModel(**movie.dict(), id_movie=id_movie, url=url)
        movie.release_date = str(movie.release_date)
        result = self._mongo_service.create_movie(movie.dict())
        if not result:
            raise ErrorResponse(
                "Failed to create movie. Try again",
                self.transaction_id,
                500
            )
        return SuccessResponse({"status": "Movie created with success"}, 200, self.transaction_id)
