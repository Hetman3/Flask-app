from database import create_table, insert_payment
from flask import Flask, request, jsonify
import os
import base64
import hashlib
import json
from multiprocessing import Process

app = Flask(__name__)
PRIVATE_KEY = os.getenv("LIQPAY_PRIVATE_KEY")

@app.route("/")
def index():
    return "Flask + LiqPay callback is running!"

@app.route("/liqpay_callback", methods=["POST"])
def liqpay_callback():
    data = request.form.get("data")
    signature = request.form.get("signature")

    if not data or not signature:
        return "Missing", 400

    sign = base64.b64encode(hashlib.sha1((PRIVATE_KEY + data + PRIVATE_KEY).encode()).digest()).decode()

    if sign != signature:
        return "Invalid signature", 403

    decoded = json.loads(base64.b64decode(data).decode())
    print("LiqPay callback received:")
    print(json.dumps(decoded, indent=2, ensure_ascii=False))

    return jsonify({"status": "ok"}), 200

def run_flask():
   app.run(debug=True, host="0.0.0.0", port=5000)

if __name__ == '__main__':
    flask_process = Process(target=run_flask)
    flask_process.start()
    flask_process.join()
