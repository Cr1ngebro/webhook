from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        r = requests.post(url, json=payload)
        print("Telegram:", r.status_code, r.text)
    except Exception as e:
        print(f"Ошибка отправки Telegram: {e}")

@app.route('/webhook/ozan', methods=['POST'])
def ozan_webhook():
    try:
        data = request.get_json(force=True)  # ✅ гарантированно dict
        print("Ozan JSON:", data)

        event_type = data.get("event", "unknown")
        transaction_id = data.get("transaction_id", "N/A")
        amount = data.get("amount", "N/A")

        msg = f"📬 Ozan событие:\n*Тип:* `{event_type}`\n*Транзакция:* `{transaction_id}`\n*Сумма:* `{amount}`"
        send_telegram_message(msg)
        return '', 200
    except Exception as e:
        print("Ошибка обработки webhook:", e)
        return 'Error', 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
