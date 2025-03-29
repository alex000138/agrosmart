from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.variety import Variety

class VarietyRepository(ABC):
    """Абстрактный репозиторий для работы с сортами"""
    
    @abstractmethod
    def get_by_id(self, variety_id: int) -> Optional[Variety]:
        """Получить сорт по ID"""
        pass

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Variety]:
        """Получить сорт по коду"""
        pass

    @abstractmethod
    def get_all(self) -> List[Variety]:
        """Получить все сорта"""
        pass

    @abstractmethod
    def add(self, variety: Variety) -> Variety:
        """Добавить новый сорт"""
        pass

    @abstractmethod
    def update(self, variety: Variety) -> None:
        """Обновить существующий сорт"""
        pass

    @abstractmethod
    def delete(self, variety_id: int) -> None:
        """Удалить сорт"""
        pass

    @abstractmethod
    def get_high_yield_varieties(self) -> List[Variety]:
        """Получить сорта с урожайностью выше среднего"""
        pass

    @abstractmethod
    def get_expiring_patents(self) -> List[Variety]:
        """Получить сорта с истекающими патентами"""
        pass
