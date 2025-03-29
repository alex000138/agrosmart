from sqlalchemy.orm import Session
from backend.domain.repositories.variety_repository import VarietyRepository
from backend.infrastructure.repositories.sqlalchemy_variety_repository import SQLAlchemyVarietyRepository

class RepositoryFactory:
    """Фабрика для создания репозиториев"""
    
    def __init__(self, session: Session):
        self.session = session

    def create_variety_repository(self) -> VarietyRepository:
        """Создает репозиторий для работы с сортами"""
        return SQLAlchemyVarietyRepository(self.session)
