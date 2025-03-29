from dependency_injector import containers, providers
from sqlalchemy.orm import Session
from infrastructure.repositories.repository_factory import RepositoryFactory
from application.use_cases.variety_management import VarietyManagementUseCase

class ApplicationContainer(containers.DeclarativeContainer):
    """Контейнер зависимостей приложения"""
    
    # Конфигурация
    config = providers.Configuration()
    
    # Репозитории
    repository_factory = providers.Factory(
        RepositoryFactory,
        session=providers.Object()  # Будет установлен извне
    )
    
    # Use Cases
    variety_management = providers.Factory(
        VarietyManagementUseCase,
        variety_repository=repository_factory.provide().create_variety_repository()
    )
