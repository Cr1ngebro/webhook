from flask import Flask, request
import requests
import json
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=data)
        print("Telegram response:", response.text)
    except Exception as e:
        print("Telegram send error:", e)


@app.route('/webhook/ozan', methods=['POST'])
def ozan_webhook():
    try:
        print("📥 Получен POST-запрос на /webhook/ozan")
        data = request.get_json(force=True)
        if isinstance(data, str):
            data = json.loads(data)
        print("📦 JSON от Ozan:", data)

        event_type = data.get("event", "unknown")
        transaction_id = data.get("transaction_id", "N/A")
        amount = data.get("amount", "N/A")

        msg = (
            f"📬 *Ozan событие:*
"
            f"*Тип:* `{event_type}`
"
            f"*Транзакция:* `{transaction_id}`
"
            f"*Сумма:* `{amount}`"
        )
        send_telegram_message(msg)

        return '', 200

    except Exception as e:
        print("❌ Ошибка в обработчике webhook:", e)
        return 'Internal Server Error', 500


@app.route("/", methods=["GET"])
def index():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
