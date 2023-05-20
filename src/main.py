from shared.infrastructure import ErrorResponse, error_exception_handler, parameter_exception_handler
from fastapi.exceptions import RequestValidationError
from shared.infrastructure import get_settings
from fastapi.openapi.utils import get_openapi
from worker.infrastructure import router
from fastapi import FastAPI
import container
import uvicorn


description = """

    Creado con FastAPI y Arquitectura Hexagonal.
    Python: 3.11.0

**Microservicio encargado de la manipulación de catálogos de películas.**

"""

settings = get_settings()
api_version = settings.API_VERSION
namespace = settings.NAMESPACE

tags = [
    {
        "name": "Health Check",
        "description": "Disponibilidad del servicio y recursos externos"
    },
    {
        "name": "Movies",
        "description": "Gestión de catálogos de películas"
    }
]

app = FastAPI(
    title="Movies",
    description=description,
    version="1.0.0",
    openapi_tags=tags,
    docs_url=f"/{namespace}/{api_version}/movies/docs",
    openapi_url=f"/{namespace}/{api_version}/movies/openapi.json",
    redoc_url=f"/{namespace}/{api_version}/movies/redoc"
)


def custom_openapi() -> dict:
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers
        )
        for method_item in app.openapi_schema.get("paths").values():
            for param in method_item.values():
                responses = param.get("responses")
                if "422" in responses:
                    del responses["422"]

    return app.openapi_schema


app.add_exception_handler(ErrorResponse, error_exception_handler)
app.add_exception_handler(RequestValidationError, parameter_exception_handler)
app.include_router(router)
app.openapi = custom_openapi
container.SingletonContainer.init()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
