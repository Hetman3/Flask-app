from flask import Flask, request, jsonify
import os
import base64
import hashlib
import json
from database import create_table, insert_payment  # Імпорт функцій для роботи з БД

# Ініціалізація Flask-додатку
app = Flask(__name__)

# Отримання приватного ключа з змінної середовища
PRIVATE_KEY = os.getenv("LIQPAY_PRIVATE_KEY")

# Створення таблиці у базі при старті додатку
create_table()

# Роут для перевірки доступності додатку
@app.route("/")
def index():
    return "Flask + LiqPay callback is running!"

# Роут для обробки POST-запиту від LiqPay після платежу
@app.route("/liqpay_callback", methods=["POST"])
def liqpay_callback():
    # Отримуємо data та signature з POST-запиту
    data = request.form.get("data")
    signature = request.form.get("signature")

    if not data or not signature:
        return "Missing parameters", 400

    # Генеруємо підпис локально для перевірки
    sign_str = PRIVATE_KEY + data + PRIVATE_KEY
    expected_signature = base64.b64encode(hashlib.sha1(sign_str.encode()).digest()).decode()

    # Перевіряємо, чи підпис відповідає
    if signature != expected_signature:
        return "Invalid signature", 403

    try:
        # Декодуємо JSON-обʼєкт
        decoded = json.loads(base64.b64decode(data).decode())
        print("LiqPay callback received:")
        print(json.dumps(decoded, indent=2, ensure_ascii=False))

        # Зберігаємо платіж у базу даних
        insert_payment(decoded)

    except Exception as e:
        print(f"Error decoding or inserting data: {e}")
        return "Internal error", 500

    return jsonify({"status": "ok"}), 200

# Запускаємо Flask-сервер на 5000 порту (очікуваний Railway)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
