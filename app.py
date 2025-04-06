from flask import Flask, request, jsonify
import os
import base64
import hashlib
import json
from database import insert_payment, create_table

# Ініціалізація Flask-додатку
app = Flask(__name__)

# Отримуємо приватний ключ із змінної середовища (налаштована в Railway)
PRIVATE_KEY = os.getenv("LIQPAY_PRIVATE_KEY")

# Створюємо таблицю у базі даних при старті додатку
create_table()

# Головна сторінка для перевірки, що додаток працює
@app.route("/")
def home():
    return "LiqPay Flask Integration is running."

# Обробник callback-запиту від LiqPay
@app.route("/liqpay_callback", methods=["POST"])
def liqpay_callback():
    # Отримуємо base64-кодовані дані та підпис із форми
    data = request.form.get("data")
    signature = request.form.get("signature")

    # Підписуємо локально, щоб перевірити достовірність
    sign_str = PRIVATE_KEY + data + PRIVATE_KEY
    expected_signature = base64.b64encode(hashlib.sha1(sign_str.encode()).digest()).decode()

    if signature != expected_signature:
        return "Invalid signature", 400

    # Декодуємо JSON-дані з base64
    decoded_data = json.loads(base64.b64decode(data).decode())

    # Зберігаємо ці дані у базу
    insert_payment(decoded_data)

    return jsonify({"status": "saved"}), 200
