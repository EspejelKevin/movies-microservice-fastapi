from shared.infrastructure import HttpResponse, get_settings, ErrorResponse
from ..infrastructure import WorkerController
from ..domain import MovieModelIn, QueryFilterModel
from fastapi import APIRouter, Depends, Body, UploadFile, File
import pathlib
import uuid


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
async def create_movie(movie: MovieModelIn = Body(...), file: UploadFile = File(...)) -> HttpResponse:
    try:
        unique_id = str(uuid.uuid4().hex)
        image_format = file.content_type.split("/")[-1]
        image_name = f"{unique_id}.{image_format}"
        url = f"{pathlib.Path(__file__).cwd()}/src/static/{image_name}"
        with open(url, "wb") as image:
            content = await file.read()
            image.write(content)
    except Exception:
        raise ErrorResponse(
            message="Failed to upload image. Try again",
            transaction_id=str(uuid.uuid4()),
            status_code=500
        )
    return WorkerController.create_movie(movie, f"static/{image_name}")


@router.get("/movies/{id_movie:int}", tags=["Movies"], summary="Obtener una película por ID")
def get_movie(id_movie:int) -> HttpResponse:
    return WorkerController.get_movie(id_movie)


@router.put("/movies/{id_movie:int}", tags=["Movies"], summary="Actualizar una película por ID")
def update_movie(id_movie:int, movie: MovieModelIn) -> HttpResponse:
    return WorkerController.update_movie(id_movie, movie)


@router.delete("/movies/{id_movie:int}", tags=["Movies"], summary="Eliminar una película por ID")
def delete_movie(id_movie:int) -> HttpResponse:
    return WorkerController.delete_movie(id_movie)
