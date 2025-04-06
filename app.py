from flask import Flask, request, jsonify
import os
import base64
import hashlib
import json

app = Flask(__name__)
PRIVATE_KEY = os.getenv("LIQPAY_PRIVATE_KEY")

@app.route("/")
def index():
    return "LiqPay Flask is running!"

@app.route("/liqpay_callback", methods=["POST"])
def callback():
    data = request.form.get("data")
    signature = request.form.get("signature")

    if not data or not signature:
        return "Missing", 400

    sign = base64.b64encode(hashlib.sha1((PRIVATE_KEY + data + PRIVATE_KEY).encode()).digest()).decode()

    if sign != signature:
        return "Invalid signature", 403

    decoded = json.loads(base64.b64decode(data).decode())
    print("LiqPay payment callback:")
    print(json.dumps(decoded, indent=2, ensure_ascii=False))

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
