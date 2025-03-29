import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from datetime import date
from ..extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Variety(db.Model):
    __tablename__ = 'varieties'
    
    id = db.Column(db.Integer, primary_key=True)
    name_main = db.Column(db.String(100), nullable=False)
    type_main = db.Column(db.String(50))
    code = db.Column(db.String(20), unique=True)
    description = db.Column(db.Text)
    origin = db.Column(db.String(100))
    registration_year = db.Column(db.Integer)
    
    # Основные связи
    disease_resistances = relationship('DiseaseResistance', back_populates='variety')
    growing_regions = relationship('GrowingRegion', back_populates='variety')
    yields = relationship('Yield', back_populates='variety')

    def __repr__(self):
        return f'<Variety {self.name_main}>'

class Disease(db.Model):
    __tablename__ = 'diseases'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)

class DiseaseResistance(db.Model):
    __tablename__ = 'disease_resistances'
    
    id = db.Column(db.Integer, primary_key=True)
    variety_id = db.Column(db.Integer, ForeignKey('varieties.id'))
    disease_id = db.Column(db.Integer, ForeignKey('diseases.id'))
    resistance_level = db.Column(db.String(50))
    
    variety = relationship('Variety', back_populates='disease_resistances')
    disease = relationship('Disease', back_populates='resistances')

class Yield(db.Model):
    __tablename__ = 'yields'
    
    id = db.Column(db.Integer, primary_key=True)
    variety_id = db.Column(db.Integer, ForeignKey('varieties.id'))
    average_yield = db.Column(db.Float)
    measurement_year = db.Column(db.Integer)
    
    variety = relationship('Variety', back_populates='yields')

class Region(db.Model):
    __tablename__ = 'regions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    climate_zone = db.Column(db.String(50))

class GrowingRegion(db.Model):
    __tablename__ = 'growing_regions'
    
    id = db.Column(db.Integer, primary_key=True)
    variety_id = db.Column(db.Integer, ForeignKey('varieties.id'))
    region_id = db.Column(db.Integer, ForeignKey('regions.id'))
    suitability_score = db.Column(db.Integer)
    
    variety = relationship('Variety', back_populates='growing_regions')
    region = relationship('Region', back_populates='varieties')