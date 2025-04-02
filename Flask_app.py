import os
import asyncio
import json
import base64
import hashlib
from flask import Flask, request
from multiprocessing import Process

# Ініціалізація Flask сервера
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, this is the Psychobot server!"

@app.route('/callback', methods=['POST'])
def liqpay_callback():
    data = request.form['data']
    signature = request.form['signature']
    
    # Перевірка підпису
    sign_string = os.getenv("LIQPAY_PRIVATE_KEY") + data + os.getenv("LIQPAY_PRIVATE_KEY")
    expected_signature = base64.b64encode(hashlib.sha1(sign_string.encode('utf-8')).digest()).decode('utf-8')
    
    if signature != expected_signature:
        return "Signature mismatch", 403
    
    # Обробка даних платежу
    payment_data = json.loads(base64.b64decode(data).decode('utf-8'))
    order_id = payment_data['order_id']
    status = payment_data['status']
    user_id = int(order_id.split('-')[1]) # Витягаємо user_id з order_id

    # Оновлення статусу платежу в базі даних
    asyncio.run(update_payment_status(order_id, status))
    
    return "Callback received", 200

async def update_payment_status(order_id, status):
    pool = await asyncpg.create_pool(os.getenv("DATABASE_URL"))
    async with pool.acquire() as conn:
        try:
            await conn.execute("UPDATE payment_orders SET payment_status = $1 WHERE order_id = $2", status, order_id)
            print(f"✅ Payment status updated to {status} for order {order_id}")
        except Exception as e:
            print(f"❌ Error updating payment status: {e}")

# Запуск Flask сервера
def run_flask():
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    run_flask()
