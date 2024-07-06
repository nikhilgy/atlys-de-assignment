CREATE TABLE historical_stock_prices (
    id SERIAL PRIMARY KEY,
    "Date" DATE NOT NULL,
    "Company" VARCHAR(255) NOT NULL,
    "Open" NUMERIC(20, 2) NOT NULL,
    "Close" NUMERIC(20, 2) NOT NULL,
    "High" NUMERIC(20, 2) NOT NULL,
    "Low" NUMERIC(20, 2) NOT NULL,
    "Volume" BIGINT NOT NULL,
    CONSTRAINT unique_date_company UNIQUE ("Date", "Company")
);