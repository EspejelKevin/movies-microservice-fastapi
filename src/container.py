from worker.application import (
    GetMoviesUseCase,
    CreateMovieUseCase,
    MongoService,
    GetMovieUseCase,
    UpdateMovieUseCase,
    DeleteMovieUseCase,
    ReadinessUseCase
)
from shared.infrastructure import MongoDatabase, Settings
from worker.infrastructure import MongoWorkerRepository
from dependency_injector import containers, providers
from contextlib import contextmanager
from typing import Optional


class RepositoriesContainer(containers.DeclarativeContainer):
    settings = providers.Dependency(Settings)
    mongo_db = providers.Singleton(
        MongoDatabase,
        db_uri=settings.provided.MONGO_URI,
        max_pool_size=settings.provided.MONGO_MAX_POOL_SIZE,
        timeout=settings.provided.MONGO_TIMEOUT_MS
    )
    mongo_worker_repository = providers.Singleton(MongoWorkerRepository, session_factory=mongo_db.provided.session)


class ServicesContainer(containers.DeclarativeContainer):
    repositories: RepositoriesContainer = providers.DependenciesContainer()
    mongo_service = providers.Factory(MongoService, mongo_repository=repositories.mongo_worker_repository)


class UseCasesContainer(containers.DeclarativeContainer):
    services: ServicesContainer = providers.DependenciesContainer()
    settings = providers.Dependency(Settings)
    get_movies = providers.Factory(GetMoviesUseCase, mongo_service=services.mongo_service)
    create_movie = providers.Factory(CreateMovieUseCase, mongo_service=services.mongo_service)
    get_movie = providers.Factory(GetMovieUseCase, mongo_service=services.mongo_service)
    update_movie = providers.Factory(UpdateMovieUseCase, mongo_service=services.mongo_service)
    delete_movie = providers.Factory(DeleteMovieUseCase, mongo_service=services.mongo_service)
    readiness = providers.Factory(ReadinessUseCase, mongo_service=services.mongo_service)


class AppContainer(containers.DeclarativeContainer):
    settings = providers.ThreadSafeSingleton(Settings)
    repositories = providers.Container(RepositoriesContainer, settings=settings)
    services = providers.Container(ServicesContainer, repositories=repositories)
    usecases = providers.Container(UseCasesContainer, services=services, settings=settings)


class SingletonContainer:
    container: Optional[AppContainer] = None

    @classmethod
    @contextmanager
    def scope(cls):
        try:
            cls.container.services.init_resources()
            yield cls.container
        finally:
            cls.container.services.shutdown_resources()

    @classmethod
    def init(cls):
        if cls.container is None:
            cls.container = AppContainer()
