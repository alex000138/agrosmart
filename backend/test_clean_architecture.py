import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from application.container import ApplicationContainer
from domain.entities.variety import Variety

# Инициализация БД
engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
session = Session()

# Создание таблиц (упрощенный вариант)
from backend.app.models.models import Base
Base.metadata.create_all(engine)

# Настройка DI контейнера
container = ApplicationContainer()
container.repository_factory.override_args.session = session

# Получение use case
variety_uc = container.variety_management()

# Тест 1: Регистрация нового сорта
try:
    new_variety = variety_uc.register_variety(
        name="Тестовый сорт",
        culture="Пшеница",
        group="Озимая",
        code="TEST001"
    )
    print(f"✅ Успешно зарегистрирован сорт: {new_variety.name}")
except Exception as e:
    print(f"❌ Ошибка регистрации: {str(e)}")

# Тест 2: Обновление патента
try:
    updated = variety_uc.update_variety_patent(
        variety_id=1,
        patent_number="PAT123",
        expiry_date=date.today() + timedelta(days=365)
    )
    print(f"✅ Успешно обновлен патент для сорта ID {updated.id}")
except Exception as e:
    print(f"❌ Ошибка обновления патента: {str(e)}")

# Тест 3: Проверка истекающих патентов
try:
    expiring = variety_uc.get_expiring_patents()
    print(f"✅ Найдено {len(expiring)} сортов с истекающими патентами")
except Exception as e:
    print(f"❌ Ошибка проверки патентов: {str(e)}")

# Тест 4: Проверка валидации кода
try:
    # Должен вызвать ошибку (код в нижнем регистре)
    variety_uc.register_variety(
        name="Невалидный сорт",
        culture="Пшеница", 
        group="Яровая",
        code="invalid"
    )
    print("❌ Не обнаружена ошибка валидации кода")
except ValueError as e:
    print(f"✅ Корректно обработана ошибка валидации: {str(e)}")

# Тест 5: Получение всех сортов
try:
    varieties = variety_uc.repository.get_all()
    print(f"✅ Успешно получено {len(varieties)} сортов")
    if varieties:
        print(f"Первый сорт: {varieties[0].name} (ID: {varieties[0].id})")
except Exception as e:
    print(f"❌ Ошибка получения списка сортов: {str(e)}")

# Тест 6: Проверка бизнес-логики патента
test_variety = Variety(
    id=999,
    name="Тест патента",
    culture="Пшеница",
    group="Яровая",
    code="TEST999",
    patent_expiry=date.today() - timedelta(days=1)  # Просроченный патент
)
print(f"Патент просрочен: {'✅' if test_variety.is_patent_expired() else '❌'}")
