-- 1. Company Wise Daily Variation of Prices

SELECT 
    Company, 
    Date, 
    (Close - Open) AS Daily_Variation
FROM 
    historical_stock_prices
ORDER BY 
    Company, Date;

-- 2. Company Wise Daily Volume Change

SELECT
    Company,
    Date,
    Volume,
    LAG(Volume, 1) OVER (PARTITION BY Company ORDER BY Date) AS Previous_Day_Volume,
    (Volume - LAG(Volume, 1) OVER (PARTITION BY Company ORDER BY Date)) AS Volume_Change
FROM
    historical_stock_prices
ORDER BY
    Company, Date;


-- 3. Median Daily Variation

WITH RankedPrices AS (
    SELECT
        Company,
        Date,
        (Close - Open) AS Daily_Variation,
        ROW_NUMBER() OVER (PARTITION BY Company ORDER BY (Close - Open)) AS rnk,
        COUNT(*) OVER (PARTITION BY Company) AS cnt
    FROM
        historical_stock_prices
)
SELECT
    Company,
    ROUND(AVG(Daily_Variation), 2) AS Median_Daily_Variation
FROM
    RankedPrices
WHERE
    rnk IN (FLOOR((cnt + 1) / 2.0), CEILING((cnt + 1) / 2.0))
GROUP BY
    Company;