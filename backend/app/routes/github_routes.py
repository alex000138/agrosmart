from flask import Blueprint, request, jsonify
import hmac
import hashlib
import subprocess
import os

github_bp = Blueprint('github', __name__, url_prefix='/github')

WEBHOOK_SECRET = os.getenv('GITHUB_WEBHOOK_SECRET', 'your_secret_here')

@github_bp.route('/webhook', methods=['POST'])
def handle_webhook():
    # Простейшая проверка секрета (можно временно отключить)
    if WEBHOOK_SECRET:
        signature = request.headers.get('X-Hub-Signature-256')
        if not signature:
            return jsonify({"error": "Missing signature"}), 403
            
        body = request.get_data()
        computed_hash = hmac.new(
            WEBHOOK_SECRET.encode(),
            body,
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(signature, f"sha256={computed_hash}"):
            return jsonify({"error": "Invalid signature"}), 403

    # Автоматический pull и перезагрузка
    if request.json.get('ref') == 'refs/heads/main':
        try:
            subprocess.run(['git', 'pull'], check=True)
            # Для Flask в development
            os.system('pkill -f "flask run" && nohup flask run &')
            return jsonify({"status": "Updated successfully!"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"status": "Ignored event"})
