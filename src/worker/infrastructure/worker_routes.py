from shared.infrastructure import HttpResponse, get_settings
from ..infrastructure import WorkerController
from ..domain import MovieModelIn, QueryFilterModel
from fastapi import APIRouter, Depends


settings = get_settings()
api_version = settings.API_VERSION
namespace = settings.NAMESPACE
path_base = f"/{namespace}/{api_version}"
router = APIRouter(prefix=path_base)


@router.get("/movies/liveness", tags=["Health Check"], summary="Estado actual del servicio")
def liveness():
    return {"status": "success"}


@router.get("/movies/readiness", tags=["Health Check"], summary="Disponibilidad de los recursos externos")
def readiness():
    return WorkerController.readiness()


@router.get("/movies", tags=["Movies"], summary="Obtener un listado de películas")
def get_movies(query_params: QueryFilterModel = Depends()) -> HttpResponse:
    return WorkerController.get_movies(query_params)


@router.post("/movies", tags=["Movies"], summary="Crear una película")
def create_movie(movie: MovieModelIn) -> HttpResponse:
    url = ""
    return WorkerController.create_movie(movie, url)


@router.get("/movies/{id_movie:int}", tags=["Movies"], summary="Obtener una película por ID")
def get_movie(id_movie:int) -> HttpResponse:
    return WorkerController.get_movie(id_movie)


@router.put("/movies/{id_movie:int}", tags=["Movies"], summary="Actualizar una película por ID")
def update_movie(id_movie:int, movie: MovieModelIn) -> HttpResponse:
    return WorkerController.update_movie(id_movie, movie)


@router.delete("/movies/{id_movie:int}", tags=["Movies"], summary="Eliminar una película por ID")
def delete_movie(id_movie:int) -> HttpResponse:
    return WorkerController.delete_movie(id_movie)
