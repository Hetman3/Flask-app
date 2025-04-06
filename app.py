from flask import Flask, request, jsonify
import os
import base64
import hashlib
import json
from database import insert_payment, create_table

app = Flask(__name__)

PRIVATE_KEY = os.getenv("LIQPAY_PRIVATE_KEY")

# Ініціалізація бази
create_table()

@app.route("/")
def home():
    print("=== / (home) route HIT ===")
    return "LiqPay Flask Integration is running."

@app.route("/liqpay_callback", methods=["POST"])
def liqpay_callback():
    print("=== /liqpay_callback HIT ===")

    data = request.form.get("data")
    signature = request.form.get("signature")

    if not data or not signature:
        return "Missing parameters", 400

    # Перевірка підпису
    sign_str = PRIVATE_KEY + data + PRIVATE_KEY
    expected_signature = base64.b64encode(hashlib.sha1(sign_str.encode()).digest()).decode()

    if signature != expected_signature:
        print("=== Invalid signature ===")
        return "Invalid signature", 403

    decoded_data = json.loads(base64.b64decode(data).decode())
    insert_payment(decoded_data)

    return jsonify({"status": "saved"}), 200

# Запуск сервера
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
