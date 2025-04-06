import os
import psycopg2
import json

def get_db_connection():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id SERIAL PRIMARY KEY,
            order_id TEXT,
            status TEXT,
            amount NUMERIC,
            currency TEXT,
            payment_id BIGINT,
            raw_data JSONB
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

def insert_payment(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO payments (order_id, status, amount, currency, payment_id, raw_data)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (
        data.get("order_id"),
        data.get("status"),
        data.get("amount"),
        data.get("currency"),
        data.get("payment_id"),
        json.dumps(data)
    ))

    conn.commit()
    cursor.close()
    conn.close()
