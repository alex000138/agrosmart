import time
import requests
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.base_url = "https://openrouter.ai/api/v1"
        self.default_model = "deepseek/deepseek-chat-v3-0324:free"
        self.default_timeout = 10  # Таймаут по умолчанию
    
    def ask_ai(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_retries: int = 3,
        system_message: Optional[str] = None
    ) -> Optional[str]:
        """
        Улучшенный метод для запросов к AI
        
        :param prompt: Текст запроса
        :param model: Модель AI (по умолчанию deepseek-chat-v3)
        :param temperature: Креативность ответов (0.0-1.0)
        :param max_retries: Максимальное количество попыток
        :param system_message: Кастомное системное сообщение
        :return: Ответ от AI или None при ошибке
        """
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY не найден в .env")

        model = model or self.default_model
        system_message = system_message or (
            "Ты - AI ассистент для сельскохозяйственного проекта AgroSmart. "
            "Отвечай на языке пользователя."
        )

        for attempt in range(max_retries):
            try:
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "HTTP-Referer": "https://github.com/alex000138/agrosmart",
                        "X-Title": "AgroSmart AI",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": temperature
                    },
                    timeout=self.default_timeout
                )
                
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]
                
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    raise RuntimeError(f"AI request failed after {max_retries} attempts: {str(e)}")
                time.sleep(1 * (attempt + 1))  # Экспоненциальная задержка


# Инициализация сервиса для использования в приложении
ai_service = AIService()
