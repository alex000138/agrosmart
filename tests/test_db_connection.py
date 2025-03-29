import os
import pytest
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture
def db_connection():
    engine = create_engine(os.getenv('DATABASE_URL'))
    conn = engine.connect()
    yield conn
    conn.close()

def test_db_connection(db_connection):
    assert db_connection is not None
    print("\n✅ Успешное подключение к PostgreSQL!")

def test_database_tables(db_connection):
    inspector = inspect(db_connection)
    tables = inspector.get_table_names()
    assert len(tables) > 0, "В базе данных отсутствуют таблицы"
    print(f"Обнаружены таблицы: {tables}")
