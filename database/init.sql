-- db/init.sql
CREATE TABLE IF NOT EXISTS stocks_import (
    date DATE,
    ticker TEXT NOT NULL,
    company_name TEXT NOT NULL,
    price NUMERIC NOT NULL,
    volume BIGINT NOT NULL,
    import_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS stocks_staging (
    date DATE,
    ticker TEXT NOT NULL,
    company_name TEXT NOT NULL,
    price NUMERIC NOT NULL,
    volume BIGINT NOT NULL,
    import_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Function to copy new unique rows from import to staging
CREATE OR REPLACE FUNCTION transfer_to_staging() RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM stocks_staging
        WHERE ticker = NEW.ticker
        AND date = NEW.date
    ) THEN
        INSERT INTO stocks_staging (date, ticker, company_name, price, volume, import_ts)
        VALUES (NEW.date, NEW.ticker, NEW.company_name, NEW.price, NEW.volume, NEW.import_ts);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger setup
DROP TRIGGER IF EXISTS trg_transfer_to_staging ON stocks_import;
CREATE TRIGGER trg_transfer_to_staging
AFTER INSERT ON stocks_import
FOR EACH ROW
EXECUTE FUNCTION transfer_to_staging();
