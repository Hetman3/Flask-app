from flask import Flask, request, jsonify
import os
import base64
import hashlib
import json
from database import insert_payment, create_table

app = Flask(__name__)

# Завантажуємо приватний ключ з .env / Railway Variables
PRIVATE_KEY = os.getenv("LIQPAY_PRIVATE_KEY")

# Створюємо таблицю при запуску (один раз)
create_table()

@app.route("/")
def home():
    return "LiqPay Flask Integration is running."

@app.route("/liqpay_callback", methods=["POST"])
def liqpay_callback():
    data = request.form.get("data")
    signature = request.form.get("signature")

    # Перевіряємо підпис LiqPay
    sign_str = PRIVATE_KEY + data + PRIVATE_KEY
    expected_signature = base64.b64encode(hashlib.sha1(sign_str.encode()).digest()).decode()

    if signature != expected_signature:
        return "Invalid signature", 400

    # Декодуємо data з base64
    decoded_data = json.loads(base64.b64decode(data).decode())

    # Зберігаємо в базу
    insert_payment(decoded_data)

    return jsonify({"status": "saved"}), 200

# Запуск у продакшн-режимі на Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway передає свій порт
    app.run(host="0.0.0.0", port=port)
