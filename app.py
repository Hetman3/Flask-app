from flask import Flask, request, jsonify
import os
import base64
import hashlib
import json
from database import create_table, insert_payment  # Підключення БД

# Ініціалізація Flask-додатку
app = Flask(__name__)
PRIVATE_KEY = os.getenv("LIQPAY_PRIVATE_KEY")

# Створення таблиці у базі при запуску додатку
create_table()

# Головна сторінка для перевірки роботи сервера
@app.route("/")
def index():
    return "Flask + LiqPay callback is running (prod WSGI)."

# Callback від LiqPay
@app.route("/liqpay_callback", methods=["POST"])
def liqpay_callback():
    data = request.form.get("data")
    signature = request.form.get("signature")

    if not data or not signature:
        return "Missing parameters", 400

    sign_str = PRIVATE_KEY + data + PRIVATE_KEY
    expected_signature = base64.b64encode(hashlib.sha1(sign_str.encode()).digest()).decode()

    if signature != expected_signature:
        return "Invalid signature", 403

    try:
        decoded = json.loads(base64.b64decode(data).decode())
        print("LiqPay callback received:")
        print(json.dumps(decoded, indent=2, ensure_ascii=False))
        insert_payment(decoded)
    except Exception as e:
        print(f"Error decoding or inserting data: {e}")
        return "Internal error", 500

    return jsonify({"status": "ok"}), 200

# Більше не потрібно app.run()
