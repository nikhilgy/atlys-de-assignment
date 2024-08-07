# atlys-de-assignment

This repository contains a Python scripts developed focusing on fetching and storing historical daily stock market data from the Alpha Vantage API. The project includes scripts to fetch data for top 10 Indian companies by market capitalization, store it in a PostgreSQL database, and optimize database querying with indexed tables. Additionally, it features SQL queries for analyzing daily price variations, volume changes, and computing median variations efficiently.


## Getting Started

1. **Installation**:
   - Clone this repository to your local machine.
   - Install Python dependencies using [Poetry](https://python-poetry.org/):
     ```bash
     poetry shell
     ```

2. **Configuration**:
   - Set up your PostgreSQL database and credentials.
   - Obtain an API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key) and add it to `.env` file.

3. **Database Setup**:
   - Execute `stock_market_db.sql` to create necessary database tables and indexes.

4. **Running Scripts**:
   - Modify `fetch_historical_data.py` and `daily_stock_data_dump.py` scripts as needed.
   - Execute scripts to fetch and store data:
     ```bash
     python app/fetch_historical_data.py
     python app/daily_stock_data_dump.py
     ```


5. **Queries**: Refer `queries.sql` for optimized SQL queries for data analysis and reporting.

    - **Company Wise Daily Variation of Prices** : Query to calculate the daily price variation (e.g., high-low difference) for each company.

    - **Company Wise Daily Volume Change** : Query to compute the daily change in trading volume for each company.

    - **Median Daily Variation** : Query to determine the median daily price variation across all companies.
