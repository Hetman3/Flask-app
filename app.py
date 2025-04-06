from flask import Flask, request, jsonify
import os
import base64
import hashlib
import json

app = Flask(__name__)

PRIVATE_KEY = os.getenv("LIQPAY_PRIVATE_KEY")

@app.route("/")
def home():
    return "LiqPay Flask callback is running."

@app.route("/liqpay_callback", methods=["POST"])
def liqpay_callback():
    data = request.form.get("data")
    signature = request.form.get("signature")

    if not data or not signature:
        print("❌ No data or signature received")
        return "Missing parameters", 400

    # Перевірка підпису
    sign_str = PRIVATE_KEY + data + PRIVATE_KEY
    expected_signature = base64.b64encode(hashlib.sha1(sign_str.encode()).digest()).decode()

    if signature != expected_signature:
        print("❌ Invalid signature")
        return "Invalid signature", 403

    # Розкодовуємо JSON з base64
    try:
        decoded_data = json.loads(base64.b64decode(data).decode())
        print("✅ Callback data received from LiqPay:")
        print(json.dumps(decoded_data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"❌ Error decoding data: {e}")
        return "Invalid data", 400

    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
