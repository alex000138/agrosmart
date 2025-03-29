import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения

class Config:
    """Конфигурация приложения"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:12345@localhost:5432/agrosmart1?client_encoding=utf8'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False