# -*- coding: utf-8 -*-
from openai import OpenAI
import os

# Настройки кодировки для Windows
os.environ['PYTHONIOENCODING'] = 'utf-8'

def deepseek_chat(prompt: str) -> str:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )
    
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[
            {
                "role": "user",
                "content": prompt.encode('utf-8').decode('utf-8')  # Фикс кодировки
            }
        ]
    )
    
    return response.choices[0].message.content

# Настройки (вынесите в .env)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "your-api-key-here")
YOUR_SITE_URL = "https://github.com/alex000138/agrosmart"  # Замените на свой репозиторий
YOUR_SITE_NAME = "agrosmart"  # Замените на название проекта

def deepseek_chat(prompt: str, system_message: str = None) -> str:
    """
    Отправляет запрос к DeepSeek через OpenRouter
    
    :param prompt: Запрос пользователя
    :param system_message: Системный промпт (опционально)
    :return: Ответ модели
    """
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )

    messages = []
    
    if system_message:
        messages.append({
            "role": "system",
            "content": system_message
        })
        
    messages.append({
        "role": "user",
        "content": prompt
    })

    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": YOUR_SITE_URL,
                "X-Title": YOUR_SITE_NAME,
            },
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
            timeout=15
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Пример использования
if __name__ == "__main__":
    response = deepseek_chat(
        system_message="Ты эксперт по сельскому хозяйству и IoT системам",
        prompt="Как оптимизировать полив в теплице?"
    )
    print("Ответ DeepSeek:\n", response)