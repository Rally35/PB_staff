FROM python:3.11-slim

WORKDIR /app

COPY app/ /app
COPY .env /app/.env

RUN pip install --no-cache-dir psycopg2-binary python-dotenv yfinance schedule

CMD ["python", "main.py"]

