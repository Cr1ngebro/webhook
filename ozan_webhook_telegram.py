from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Настройки Telegram-бота через переменные окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(text):
    """Отправка сообщения в Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        print("✅ Уведомление отправлено в Telegram:", response.status_code, response.text)
    except Exception as e:
        print("❌ Ошибка при отправке Telegram:", e)

@app.route('/webhook/ozan', methods=['POST'])
def ozan_webhook():
    try:
        print("📥 Получен POST-запрос на /webhook/ozan")

        # Принудительно разбираем JSON
        data = request.get_json(force=True)
        print("📦 JSON от Ozan:", data)

        event_type = data.get("event", "unknown")
        transaction_id = data.get("transaction_id", "N/A")
        amount = data.get("amount", "N/A")

        msg = (
            f"📬 *Ozan событие:*\n"
            f"*Тип:* `{event_type}`\n"
            f"*Транзакция:* `{transaction_id}`\n"
            f"*Сумма:* `{amount}`"
        )
        send_telegram_message(msg)

        return '', 200

    except Exception as e:
        print("❌ Ошибка в обработчике webhook:", e)
        return 'Internal Server Error', 500

# Фронтовая проверка
@app.route('/')
def index():
    return "Ozan Webhook API запущен ✅"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
