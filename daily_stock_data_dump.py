import time
import logging
from datetime import datetime, timedelta
import pandas as pd
from stock_data_utils import fetch_data, save_to_db, COMPANIES

YESTERDAY = datetime.now() - timedelta(days=1)
YESTERDAY_STR = YESTERDAY.strftime('%Y-%m-%d')

def main():
    all_data = []
    for company, symbol in COMPANIES.items():
        logging.info(f"Fetching data for {company} ({symbol})...")
        data = fetch_data(symbol, start_date=YESTERDAY_STR)
        if data is not None and not data.empty:
            all_data.append(data)
        else:
            logging.error("Data Retrieved: {}".format(data))
        time.sleep(15)  # Respect API rate limits

    if all_data:
        df_all = pd.concat(all_data)
        save_to_db(df_all)
        logging.info(f"Data for {YESTERDAY_STR} saved to database.")
    else:
        logging.info("No data fetched.")

if __name__ == "__main__":
    main()
