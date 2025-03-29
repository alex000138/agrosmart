import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, Column, Integer, String, Date, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class VarietyModel(Base):
    __tablename__ = 'varieties'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    culture = Column(String(100), nullable=False)
    group = Column(String(50), nullable=False)
    code = Column(String(20), nullable=False)
    description = Column(Text)
    registration_year = Column(Integer)
    patent_number = Column(String(20))
    patent_expiry = Column(Date)

# Инициализация БД
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)

# Тест 1: Создание записи
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

test_variety = VarietyModel(
    name="Тестовый сорт",
    culture="Пшеница",
    group="Озимая",
    code="TEST001"
)
session.add(test_variety)
session.commit()
print(f"✅ Успешно создан сорт: {test_variety.name} (ID: {test_variety.id})")

# Тест 2: Получение записи
found = session.query(VarietyModel).get(test_variety.id)
print(f"✅ Успешно найден сорт: {found.name if found else '❌ Не найден'}")
