from datetime import date
from agrosmart.backend.extensions import db
from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import relationship

class Variety(db.Model):
    __tablename__ = 'varieties'

    id = db.Column(db.Integer, primary_key=True)
    name_main = db.Column('name', db.String(255), nullable=False, index=True)
    type_main = db.Column('type', db.String(100))
    group = db.Column(db.String(50))
    code = db.Column(db.String(20), unique=True)
    description = db.Column(db.Text)
    origin = db.Column(db.String(100))
    registration_year = db.Column(db.Integer)
    patent_number = db.Column(db.String(20))
    patent_expiry = db.Column(db.Date)

    # Relationships
    authors = relationship('Author', secondary='variety_authors', back_populates='varieties')
    applicants = relationship('Applicant', secondary='variety_applicants', back_populates='varieties')
    regions = relationship('Region', secondary='variety_regions', back_populates='varieties')
    disease_resistances = relationship('DiseaseResistance', back_populates='variety')
    yield_data = relationship('YieldData', back_populates='variety')
    quality_parameters = relationship('QualityParameters', back_populates='variety')
    patent = relationship('Patent', uselist=False, back_populates='variety')

    def __repr__(self):
        return f'<Variety {self.name_main}>'

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    varieties = relationship('Variety', secondary='variety_authors', back_populates='authors')

class Applicant(db.Model):
    __tablename__ = 'applicants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text)

    varieties = relationship('Variety', secondary='variety_applicants', back_populates='applicants')

class Region(db.Model):
    __tablename__ = 'regions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    code = db.Column(db.String(10))

    varieties = relationship('Variety', secondary='variety_regions', back_populates='regions')
    yield_data = relationship('YieldData', back_populates='region')

class Disease(db.Model):
    __tablename__ = 'diseases'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    resistances = relationship('DiseaseResistance', back_populates='disease')

class DiseaseResistance(db.Model):
    __tablename__ = 'disease_resistances'

    id = db.Column(db.Integer, primary_key=True)
    variety_id = db.Column(db.Integer, ForeignKey('varieties.id'))
    disease_id = db.Column(db.Integer, ForeignKey('diseases.id'))
    resistance_level = db.Column(db.String(50))

    variety = relationship('Variety', back_populates='disease_resistances')
    disease = relationship('Disease', back_populates='resistances')

class YieldData(db.Model):
    __tablename__ = 'yield_data'

    id = db.Column(db.Integer, primary_key=True)
    variety_id = db.Column(db.Integer, ForeignKey('varieties.id'))
    region_id = db.Column(db.Integer, ForeignKey('regions.id'))
    average_yield = db.Column(Numeric(10, 2))
    max_yield = db.Column(Numeric(10, 2))

    variety = relationship('Variety', back_populates='yield_data')
    region = relationship('Region', back_populates='yield_data')

class QualityParameters(db.Model):
    __tablename__ = 'quality_parameters'

    id = db.Column(db.Integer, primary_key=True)
    variety_id = db.Column(db.Integer, ForeignKey('varieties.id'))
    protein_content = db.Column(Numeric(5, 2))
    gluten_content = db.Column(Numeric(5, 2))
    test_weight = db.Column(Numeric(6, 2))

    variety = relationship('Variety', back_populates='quality_parameters')

class Patent(db.Model):
    __tablename__ = 'patents'

    variety_id = db.Column(db.Integer, ForeignKey('varieties.id'), primary_key=True)
    application_num = db.Column(db.String(50))
    application_date = db.Column(db.Date)
    grant_date = db.Column(db.Date)
    fee = db.Column(Numeric(10, 2))
    fee_due_date = db.Column(db.Date)

    variety = relationship('Variety', back_populates='patent')

# Association tables
class VarietyAuthor(db.Model):
    __tablename__ = 'variety_authors'

    variety_id = db.Column(db.Integer, ForeignKey('varieties.id'), primary_key=True)
    author_id = db.Column(db.Integer, ForeignKey('authors.id'), primary_key=True)

class VarietyApplicant(db.Model):
    __tablename__ = 'variety_applicants'

    variety_id = db.Column(db.Integer, ForeignKey('varieties.id'), primary_key=True)
    applicant_id = db.Column(db.Integer, ForeignKey('applicants.id'), primary_key=True)

class VarietyRegion(db.Model):
    __tablename__ = 'variety_regions'

    variety_id = db.Column(db.Integer, ForeignKey('varieties.id'), primary_key=True)
    region_id = db.Column(db.Integer, ForeignKey('regions.id'), primary_key=True)
