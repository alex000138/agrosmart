import requests
import json

def test_ai_endpoint():
    url = "http://localhost:5000/api/ai/ask"
    payload = {
        "prompt": "Какие современные технологии используются в точном земледелии?",
        "model": "anthropic/claude-3-haiku",
        "temperature": 0.7
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    print(f"Статус: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"Ошибка: {response.text}")

if __name__ == "__main__":
    test_ai_endpoint()