from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Установите ваш Telegram токен и chat_id как переменные окружения или впишите вручную:
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "ВАШ_ТОКЕН_БОТА")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "ВАШ_CHAT_ID")

def send_telegram_message(text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"Ошибка при отправке Telegram сообщения: {e}")

@app.route("/webhook/ozan", methods=["POST"])
def ozan_webhook():
    try:
        # Преобразуем входные данные в JSON
        data = request.get_json(force=True)

        if not isinstance(data, dict):
            return jsonify({"error": "Invalid payload format"}), 400

        event_type = data.get("event")
        transaction_id = data.get("transaction_id")
        amount = data.get("amount")

        # Формируем сообщение
        message = f'📢 *Ozan событие:* `{event_type}`\n'

        if transaction_id:
            message += f'💳 *ID транзакции:* `{transaction_id}`\n'

        if amount:
            message += f'💰 *Сумма:* `{amount}`'

        send_telegram_message(message)

        return jsonify({"status": "ok"}), 200
    except Exception as e:
        send_telegram_message(f"❌ Ошибка в webhook: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return "Ozan Webhook Handler работает!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
