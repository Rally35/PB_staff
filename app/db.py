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
            # Create import table
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
            
            # Create staging table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS stock_data_staging (
                    date DATE NOT NULL,
                    ticker TEXT NOT NULL,
                    company_name TEXT,
                    price NUMERIC,
                    volume BIGINT,
                    PRIMARY KEY (date, ticker)
                );
            """)
            
            # Create procedure
            cur.execute("""
                CREATE OR REPLACE FUNCTION move_to_staging()
                RETURNS TRIGGER AS $$
                BEGIN
                    INSERT INTO stock_data_staging (date, ticker, company_name, price, volume)
                    SELECT NEW.date, NEW.ticker, NEW.company_name, NEW.price, NEW.volume
                    WHERE NOT EXISTS (
                        SELECT 1 FROM stock_data_staging
                        WHERE ticker = NEW.ticker AND date = NEW.date
                    );
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
            """)

            # Create trigger
            cur.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_trigger WHERE tgname = 'trigger_move_to_staging'
                    ) THEN
                        CREATE TRIGGER trigger_move_to_staging
                        AFTER INSERT ON stock_data
                        FOR EACH ROW
                        EXECUTE FUNCTION move_to_staging();
                    END IF;
                END
                $$;
            """)

        conn.commit()


def insert_price(ticker, company_name, price, volume):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO stock_data (date, ticker, company_name, price, volume)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (date, ticker) DO NOTHING;
            """, (date.today(), ticker, company_name, price, volume))
        conn.commit()

