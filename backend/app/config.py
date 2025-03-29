import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения

class Config:
    """Конфигурация приложения"""
    # Основные настройки
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # База данных
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:12345@localhost:5432/agrosmart1?client_encoding=utf8'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OpenRouter API
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')  # Обязательный параметр
    OPENROUTER_BASE_URL = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
    AI_MODEL_ID = os.getenv('AI_MODEL_ID', 'openai/gpt-3.5-turbo')  # Модель по умолчанию
