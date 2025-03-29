from flask import Blueprint, request, jsonify
from ..services.ai_service import ai_service
import logging
from functools import wraps

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')
logger = logging.getLogger(__name__)

def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            logger.warning("Request must be JSON")
            return jsonify({"error": "Request must be JSON"}), 415
        return f(*args, **kwargs)
    return wrapper

@ai_bp.route('/ask', methods=['POST'])
@validate_json
def ask_handler():
    """
    Обработчик AI запросов
    ---
    tags:
      - AI
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            prompt:
              type: string
              description: Текст запроса к AI
              example: "Какие культуры лучше сажать?"
            model:
              type: string
              description: Модель AI (опционально)
              example: "anthropic/claude-3-haiku"
            temperature:
              type: number
              description: Креативность ответа (0-1)
              example: 0.5
    responses:
      200:
        description: Успешный ответ AI
        schema:
          type: object
          properties:
            answer:
              type: string
            model:
              type: string
            status:
              type: string
      400:
        description: Неверный запрос
      415:
        description: Неверный формат запроса (не JSON)
      503:
        description: Ошибка сервиса AI
    """
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        answer = ai_service.ask_ai(
            prompt=prompt,
            model=data.get('model'),
            temperature=float(data.get('temperature', 0.7))
        )
        
        return jsonify({
            "answer": answer,
            "model": data.get('model') or ai_service.default_model,
            "status": "success"
        })

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"AI processing error: {str(e)}")
        return jsonify({"error": "AI service unavailable"}), 503
