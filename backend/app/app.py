import sys
import os
print("PYTHONPATH:", sys.path)
print("Current working directory:", os.getcwd())

from flask import Flask, render_template
from dotenv import load_dotenv
from flasgger import Swagger
from flask_migrate import Migrate
from agrosmart.backend.extensions import db
import os

# Загрузка переменных окружения ПЕРЕД созданием приложения
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))  # Явный путь к .env

app = Flask(__name__)

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:12345@localhost:5432/agrosmart1')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация расширений
db.init_app(app)
migrate = Migrate(app, db)

# Конфигурация Swagger
app.config['SWAGGER'] = {
    'title': 'AgroSmart API',
    'uiversion': 3,
    'specs_route': '/apidocs/'
}
swagger = Swagger(app)

# Проверка загрузки переменных
print("OPENROUTER_API_KEY exists:", "OPENROUTER_API_KEY" in os.environ)
print("Current working directory:", os.getcwd())

# Регистрация blueprints (после создания app)
from .routes.ai_routes import ai_bp
app.register_blueprint(ai_bp, url_prefix='/api/ai')

@app.errorhandler(500)
def internal_error(error):
    """Обработчик ошибок 500"""
    return render_template('500.html'), 500
