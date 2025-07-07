import os
import psycopg2
from datetime import date

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME")
    )

def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS stock_data (
                    date DATE NOT NULL,
                    ticker TEXT NOT NULL,
                    company_name TEXT,
                    price NUMERIC,
                    volume BIGINT,
                    PRIMARY KEY (date, ticker)
                );
            """)
        conn.commit()


def insert_price(ticker, company_name, price, volume):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO stock_data (date, ticker, company_name, price, volume)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (date, ticker) DO UPDATE 
                SET company_name = EXCLUDED.company_name,
                    price = EXCLUDED.price,
                    volume = EXCLUDED.volume;
                """,
                (date.today(), ticker, company_name, price, volume)
            )
        conn.commit()

