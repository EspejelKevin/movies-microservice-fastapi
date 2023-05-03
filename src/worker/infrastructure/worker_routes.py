from shared.infrastructure import HttpResponse, get_settings
from ..infrastructure import WorkerController
from ..domain import MovieModelIn, QueryFilterModel
from fastapi import APIRouter, Depends


settings = get_settings()
api_version = settings.API_VERSION
namespace = settings.NAMESPACE
path_base = f"/{namespace}/{api_version}"
router = APIRouter(prefix=path_base)


@router.get("/movies", tags=["Movies"])
def get_movies(query_params: QueryFilterModel = Depends()) -> HttpResponse:
    return WorkerController.get_movies(query_params)


@router.post("/movies", tags=["Movies"])
def create_movie(movie: MovieModelIn) -> HttpResponse:
    url = ""
    return WorkerController.create_movie(movie, url)


@router.get("/movies/{id_movie:int}", tags=["Movies"])
def get_movie(id_movie) -> HttpResponse:
    return WorkerController.get_movie(id_movie)


@router.put("/movies/{id_movie:int}", tags=["Movies"])
def update_movie(id_movie, movie: MovieModelIn) -> HttpResponse:
    return WorkerController.update_movie(id_movie, movie)


@router.delete("/movies/{id_movie:int}", tags=["Movies"])
def delete_movie(id_movie) -> HttpResponse:
    return WorkerController.delete_movie(id_movie)
