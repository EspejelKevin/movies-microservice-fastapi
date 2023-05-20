from shared.infrastructure import HttpResponse
from shared.domain import Response
from ..domain import MovieModelIn, QueryFilterModel
import container


class WorkerResponse(HttpResponse):
    def __init__(self, content: Response) -> None:
        super().__init__(
            content=content,
            status_code=content._status_code,
            excludes={"_status_code"}
        )


class WorkerController:
    @staticmethod
    def get_movies(query_params: QueryFilterModel):
        with container.SingletonContainer.scope() as app:
            usecase = app.usecases.get_movies()
            response = usecase.execute(query_params)
            return WorkerResponse(content=response)

    @staticmethod
    def create_movie(movie: MovieModelIn, url: str):
        with container.SingletonContainer.scope() as app:
            usecase = app.usecases.create_movie()
            response = usecase.execute(movie, url)
            return WorkerResponse(content=response)

    @staticmethod
    def get_movie(id_movie: int):
        with container.SingletonContainer.scope() as app:
            usecase = app.usecases.get_movie()
            response = usecase.execute(id_movie)
            return WorkerResponse(content=response)

    @staticmethod
    def update_movie(id_movie: int, movie: MovieModelIn):
        with container.SingletonContainer.scope() as app:
            usecase = app.usecases.update_movie()
            response = usecase.execute(id_movie, movie)
            return WorkerResponse(content=response)

    @staticmethod
    def delete_movie(id_movie: int):
        with container.SingletonContainer.scope() as app:
            usecase = app.usecases.delete_movie()
            response = usecase.execute(id_movie)
            return WorkerResponse(content=response)
        
    @staticmethod
    def readiness():
        with container.SingletonContainer.scope() as app:
            usecase = app.usecases.readiness()
            response = usecase.execute()
            return WorkerResponse(content=response)
