import time
import logging
from datetime import datetime
import pandas as pd
from stock_data_utils import fetch_data, save_to_db, COMPANIES

START_DATE = datetime(2020, 1, 1)
END_DATE = datetime(2024, 5, 31)
OUTPUT_FILE = "historical_stock_data.csv"

def main():
    all_data = []
    for company, symbol in COMPANIES.items():
        logging.info(f"Fetching data for {company} ({symbol})...")
        data = fetch_data(symbol, start_date=START_DATE, end_date=END_DATE)
        if data is not None:
            all_data.append(data)
        time.sleep(15)  # Due to API rate limits

    if all_data:
        df_all = pd.concat(all_data)
        df_all.to_csv(OUTPUT_FILE, index=False)
        save_to_db(df_all)
        logging.info(f"Data saved to {OUTPUT_FILE} and database.")
    else:
        logging.error("No data fetched.")

if __name__ == "__main__":
    main()
