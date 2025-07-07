import json
import time
import yfinance as yf
import schedule
from db import init_db, insert_price

def load_tickers():
    with open("config.json", "r") as f:
        return json.load(f)

def fetch_and_store():
    print("Running fetch job...")
    tickers = load_tickers()
    for symbol in tickers:
        try:
            data = yf.Ticker(symbol)
            info = data.info
            price = info.get("regularMarketPrice")
            volume = info.get("volume")
            company_name = info.get("shortName")

            if price and company_name:
                insert_price(symbol, company_name, price, volume)
                print(f"{symbol}: {price} ({volume} volume) saved.")
            else:
                print(f"{symbol}: Incomplete data, skipped.")
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")


def main():
    init_db()
    schedule.every(1).minutes.do(fetch_and_store)

    print("Scheduler started.")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
