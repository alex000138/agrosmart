# services/variety_service.py
from models import Variety
from extensions import db

class VarietyService:
    @staticmethod
    def get_latest_varieties(limit=5):
        return Variety.query.order_by(Variety.id.desc()).limit(limit).all()

    @staticmethod
    def search_varieties(query):
        return Variety.query.filter(Variety.name_main.ilike(f'%{query}%')).all()

    @staticmethod
    def add_variety(name, type_main, code, description, origin, registration_year):
        new_variety = Variety(
            name_main=name,
            type_main=type_main,
            code=code,
            description=description,
            origin=origin,
            registration_year=registration_year
        )
        db.session.add(new_variety)
        db.session.commit()
        return new_variety

    @staticmethod
    def get_variety_by_id(variety_id):
        return Variety.query.get_or_404(variety_id)