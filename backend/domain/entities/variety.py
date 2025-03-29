from datetime import date
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Variety:
    """Доменная сущность сорта пшеницы"""
    id: int
    name: str
    culture: str
    group: str
    code: str
    description: Optional[str] = None
    origin: Optional[str] = None
    registration_year: Optional[int] = None
    patent_number: Optional[str] = None
    patent_expiry: Optional[date] = None

    def is_patent_expired(self) -> bool:
        """Проверяет истек ли срок патента"""
        if not self.patent_expiry:
            return False
        return self.patent_expiry < date.today()

    def is_registered(self) -> bool:
        """Проверяет зарегистрирован ли сорт"""
        return self.registration_year is not None

    def validate_code(self) -> bool:
        """Проверяет валидность кода сорта"""
        return len(self.code) >= 3 and self.code.isalnum()
