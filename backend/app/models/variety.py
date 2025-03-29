from ..extensions import db

class Variety(db.Model):
    """Модель сорта растений"""
    __tablename__ = 'varieties'
    
    id = db.Column(db.Integer, primary_key=True)
    name_main = db.Column(db.String(100), nullable=False)
    type_main = db.Column(db.String(50))
    code = db.Column(db.String(20))
    description = db.Column(db.Text)
    origin = db.Column(db.String(100))
    registration_year = db.Column(db.Integer)
    
    def __repr__(self):
        return f"<Variety {self.name_main}>"
    
    def to_dict(self):
        """Преобразование объекта в словарь для API"""
        return {
            'id': self.id,
            'name_main': self.name_main,
            'type_main': self.type_main,
            'code': self.code,
            'description': self.description,
            'origin': self.origin,
            'registration_year': self.registration_year
        }
