import os
import asyncio
import json
import asyncpg
from flask import Flask, request
import base64
import hashlib

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
LIQPAY_PUBLIC_KEY = os.getenv("LIQPAY_PUBLIC_KEY")
LIQPAY_PRIVATE_KEY = os.getenv("LIQPAY_PRIVATE_KEY")

async def connect_to_db():
    try:
        return await asyncpg.create_pool(DATABASE_URL)
    except Exception as e:
        print(f"❌ Помилка підключення до бази даних: {e}")
        return None

@app.route('/')
def index():
    return "Hello, this is the Psychobot server!"

@app.route('/callback', methods=['POST'])
def liqpay_callback():
    data = request.form['data']
    signature = request.form['signature']
    
    sign_string = LIQPAY_PRIVATE_KEY + data + LIQPAY_PRIVATE_KEY
    expected_signature = base64.b64encode(hashlib.sha1(sign_string.encode('utf-8')).digest()).decode('utf-8')
    
    if signature != expected_signature:
        return "Signature mismatch", 403
    
    payment_data = json.loads(base64.b64decode(data).decode('utf-8'))
    order_id = payment ▋
