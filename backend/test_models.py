import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base, Variety as VarietyModel

# Инициализация БД
engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
session = Session()

# Создание таблиц
Base.metadata.create_all(engine)

# Тест 1: Создание записи
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
