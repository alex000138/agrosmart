from flask import Flask, render_template
from flask_migrate import Migrate 
from .config import Config
from agrosmart.backend.extensions import db
from dotenv import load_dotenv
import os

# Загрузка .env из корня проекта
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

def create_app():
    """Фабрика для создания экземпляра Flask приложения"""
    app = Flask(__name__, template_folder='templates')
    
    # Загрузка конфигурации
    app.config.from_object(Config)
    
    # Инициализация расширений
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Регистрация blueprint'ов
    from .routes.main import main_bp
    from .routes.ai_routes import ai_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    
    # Создание таблиц БД
    with app.app_context():
        db.create_all()
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    return app

# Создаем экземпляр приложения
app = create_app()
