import os
import psycopg2
import json

def get_db_connection():
    return psycopg2.connect(os.environ["DATABASE_URL"])

def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS liqpay_logs (
            id SERIAL PRIMARY KEY,
            order_id TEXT,
            status TEXT,
            amount TEXT,
            currency TEXT,
            payment_id BIGINT,
            raw_data JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_payment(data):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO liqpay_logs (order_id, status, amount, currency, payment_id, raw_data)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data.get("order_id"),
        data.get("status"),
        data.get("amount"),
        data.get("currency"),
        data.get("payment_id"),
        json.dumps(data)
    ))
    conn.commit()
    cur.close()
    conn.close()
