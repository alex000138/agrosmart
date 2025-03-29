from typing import Optional
from datetime import date
from domain.entities.variety import Variety
from domain.repositories.variety_repository import VarietyRepository

class VarietyManagementUseCase:
    """Use case для управления сортами пшеницы"""

    def __init__(self, variety_repository: VarietyRepository):
        self.repository = variety_repository

    def register_variety(self, name: str, culture: str, group: str, code: str) -> Variety:
        """Регистрация нового сорта с валидацией"""
        if not self._validate_variety_code(code):
            raise ValueError("Некорректный код сорта")
            
        existing = self.repository.get_by_code(code)
        if existing:
            raise ValueError("Сорт с таким кодом уже существует")

        variety = Variety(
            id=0,  # Будет установлен при сохранении
            name=name,
            culture=culture,
            group=group,
            code=code
        )

        return self.repository.add(variety)

    def update_variety_patent(self, variety_id: int, patent_number: str, expiry_date: date) -> Variety:
        """Обновление патентной информации"""
        variety = self.repository.get_by_id(variety_id)
        if not variety:
            raise ValueError("Сорт не найден")

        variety.patent_number = patent_number
        variety.patent_expiry = expiry_date
        
        self.repository.update(variety)
        return variety

    def get_expiring_patents(self) -> list[Variety]:
        """Получение сортов с истекающими патентами"""
        varieties = self.repository.get_all()
        today = date.today()
        return [v for v in varieties 
                if v.patent_expiry and v.patent_expiry > today 
                and (v.patent_expiry - today).days <= 180]

    def _validate_variety_code(self, code: str) -> bool:
        """Валидация кода сорта"""
        return len(code) >= 3 and code.isalnum() and code.isupper()
