agrosmart/
├── .vscode/                  # Настройки редактора
├── backend/                  # Бэкенд (API и логика)
│   ├── app/                  # Основное приложение
│   │   ├── __init__.py       # Инициализация Flask app
│   │   ├── models/           # Модели данных
│   │   ├── routes/           # API endpoints
│   │   ├── services/         # Бизнес-логика
│   │   ├── static/           # Статика API (если нужно)
│   │   ├── templates/        # Шаблоны для email и т.д.
│   │   ├── config.py         # Конфигурация
│   │   └── extensions.py     # Расширения Flask
│   ├── tests/                # Тесты бэкенда
│   └── requirements.txt      # Зависимости
│
├── frontend/                 # Фронтенд (отдельное приложение)
│   ├── src/                  # Исходники фронтенда
│   │   ├── assets/           # Изображения, шрифты
│   │   ├── css/              # Стили
│   │   ├── js/               # Скрипты
│   │   └── templates/        # HTML шаблоны
│   └── package.json          # Зависимости фронтенда
│
├── config/                   # Общие конфигурации
├── scripts/                  # Вспомогательные скрипты
├── .flaskenv                 # Переменные окружения Flask
├── .gitignore                # Игнорируемые файлы
└── README.md                 # Документация