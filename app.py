from flask import Flask, request, jsonify
import os
import base64
import hashlib
import json
from database import insert_payment, create_table

app = Flask(__name__)

PRIVATE_KEY = os.getenv("LIQPAY_PRIVATE_KEY")

# Створюємо таблицю при запуску
create_table()

@app.route("/")
def home():
    return "LiqPay Flask Integration is running."

@app.route("/liqpay_callback", methods=["POST"])
def liqpay_callback():
    data = request.form.get("data")
    signature = request.form.get("signature")

    # Перевірка підпису
    sign_str = PRIVATE_KEY + data + PRIVATE_KEY
    expected_signature = base64.b64encode(hashlib.sha1(sign_str.encode()).digest()).decode()

    if signature != expected_signature:
        return "Invalid signature", 400

    decoded_data = json.loads(base64.b64decode(data).decode())

    # Зберігаємо в БД
    insert_payment(decoded_data)

    return jsonify({"status": "saved"}), 200

if __name__ == "__main__":
    app.run(debug=True)
