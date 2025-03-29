from flask import Flask
from dotenv import load_dotenv
from flasgger import Swagger
import os

# Загрузка переменных окружения ПЕРЕД созданием приложения
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))  # Явный путь к .env

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
