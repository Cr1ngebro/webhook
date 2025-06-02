import requests
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        return response.ok
    except Exception as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")
        return False

@app.route("/webhook/ozan", methods=["POST"])
def ozan_webhook():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON received"}), 400
    
    event_type = data.get("event")
    msg = ""

    if event_type == "payment_success":
        transaction_id = data.get("transaction_id")
        amount = data.get("amount")
        msg = f"✅ <b>Оплата успешна</b>\nТранзакция: {transaction_id}\nСумма: {amount}"
    
    elif event_type == "payment_failure":
        transaction_id = data.get("transaction_id")
        error_code = data.get("error_code")
        msg = f"❌ <b>Оплата неуспешна</b>\nТранзакция: {transaction_id}\nОшибка: {error_code}"
        
    elif event_type == "fund_added":
        account_id = data.get("account_id")
        amount = data.get("amount")
        msg = f"➕ <b>Средства добавлены</b>\nСчет: {account_id}\nСумма: {amount}"
        
    elif event_type == "fund_withdrawn":
        account_id = data.get("account_id")
        amount = data.get("amount")
        msg = f"➖ <b>Средства списаны</b>\nСчет: {account_id}\nСумма: {amount}"
        
    elif event_type == "authorization_request":
        user_id = data.get("user_id")
        msg = f"🔐 <b>Запрос на авторизацию</b>\nПользователь: {user_id}"
        
    elif event_type == "3ds_authentication":
        transaction_id = data.get("transaction_id")
        status = data.get("status")
        msg = f"🛡️ <b>3DS авторизация</b>\nТранзакция: {transaction_id}\nСтатус: {status}"
    
    else:
        msg = f"❓ <b>Неизвестное событие</b>\nДанные: {data}"

    print(msg)
    send_telegram_message(msg)

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
