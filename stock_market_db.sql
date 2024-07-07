-- Create historical_stock_prices DB table
-- This table will store historical stock prices data
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

-- Create index on Company and Date with all price columns
-- This index will improve the performance of queries that filter by company and date and include price columns
CREATE INDEX idx_company_date_prices ON historical_stock_prices ("Company", "Date", "Open", "Close", "High", "Low");

-- Create index on Company, Date, and Volume
-- This index will improve the performance of queries that filter by company and date and involve the volume column
CREATE INDEX idx_company_date_volume ON historical_stock_prices ("Company", "Date", "Volume");

-- Create index on Company and Date
-- This index will improve the performance of general queries that filter by company and date
CREATE INDEX idx_company_date ON historical_stock_prices ("Company", "Date");
