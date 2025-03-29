from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.variety import Variety
from domain.repositories.variety_repository import VarietyRepository
from backend.app.models.models import Variety as VarietyModel

class SQLAlchemyVarietyRepository(VarietyRepository):
    """Реализация репозитория для SQLAlchemy"""

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, variety_id: int) -> Optional[Variety]:
        db_variety = self.session.query(VarietyModel).get(variety_id)
        if not db_variety:
            return None
        return self._to_domain_entity(db_variety)

    def get_by_code(self, code: str) -> Optional[Variety]:
        db_variety = self.session.query(VarietyModel).filter_by(code=code).first()
        if not db_variety:
            return None
        return self._to_domain_entity(db_variety)

    def get_all(self) -> List[Variety]:
        db_varieties = self.session.query(VarietyModel).all()
        return [self._to_domain_entity(v) for v in db_varieties]

    def add(self, variety: Variety) -> Variety:
        db_variety = VarietyModel(
            name=variety.name,
            culture=variety.culture,
            group=variety.group,
            code=variety.code,
            description=variety.description,
            origin=variety.origin,
            registration_year=variety.registration_year,
            patent_number=variety.patent_number,
            patent_expiry=variety.patent_expiry
        )
        self.session.add(db_variety)
        self.session.commit()
        return self._to_domain_entity(db_variety)

    def update(self, variety: Variety) -> None:
        db_variety = self.session.query(VarietyModel).get(variety.id)
        if db_variety:
            db_variety.name = variety.name
            db_variety.culture = variety.culture
            # ... остальные поля
            self.session.commit()

    def delete(self, variety_id: int) -> None:
        db_variety = self.session.query(VarietyModel).get(variety_id)
        if db_variety:
            self.session.delete(db_variety)
            self.session.commit()

    def _to_domain_entity(self, db_variety: VarietyModel) -> Variety:
        """Конвертирует SQLAlchemy модель в доменную сущность"""
        return Variety(
            id=db_variety.id,
            name=db_variety.name,
            culture=db_variety.culture,
            group=db_variety.group,
            code=db_variety.code,
            description=db_variety.description,
            origin=db_variety.origin,
            registration_year=db_variety.registration_year,
            patent_number=db_variety.patent_number,
            patent_expiry=db_variety.patent_expiry
        )
