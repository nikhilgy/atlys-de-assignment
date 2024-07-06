import requests
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import time
import logging
from config import ALPHA_VANTAGE_API_KEY, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

"""Configure logging"""
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    filemode='w',
    format='%(asctime)s: %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

""" #TODO List of top 10 companies in India by Market Cap"""
COMPANIES = {
    "RELIANCE": "RELIANCE.BSE",
    "TCS": "TCS.BSE",
    "HDFCBANK": "HDFCBANK.BSE",
    "ICICIBANK": "ICICIBANK.BSE",
    "BHARTIARTL": "BHARTIARTL.BSE",
    "SBIN": "SBIN.BSE",
    "INFY": "INFY.BSE",
    "LIC": "LICI.BSE",
    "HINDUNILVR": "HINDUNILVR.BSE",
    "ITC": "ITC.BSE"
}

BASE_URL = "https://www.alphavantage.co/query"
OUTPUT_FILE = "historical_stock_data.csv"

START_DATE = datetime(2020, 1, 1)
END_DATE = datetime(2024, 5, 31)

"""Create a database connection"""
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

def fetch_data(symbol):
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "full",
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        logging.info("Data: {}".format(data))
        if "Time Series (Daily)" not in data:
            logging.error(f"Error fetching data for {symbol}: {data.get('Note', 'No data returned')}")
            return None

        df = pd.DataFrame(data["Time Series (Daily)"]).T
        df.index = pd.to_datetime(df.index)
        df.columns = ["Open", "High", "Low", "Close", "Volume"]
        df = df.reset_index().rename(columns={"index": "Date"})
        df["Company"] = symbol

        """Filter the DataFrame by date range"""
        df = df[(df['Date'] >= START_DATE) & (df['Date'] <= END_DATE)]
        return df
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error for {symbol}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error for {symbol}: {e}")
        return None

def save_to_csv_and_db(dataframe, output_file, engine):
    try:
        dataframe.to_csv(output_file, index=False)
        dataframe.to_sql('historical_stock_prices', engine, if_exists='append', index=False)
        logging.info(f"Data saved to {output_file} and database.")
    except Exception as e:
        logging.error(f"Error saving data: {e}")

def main():
    all_data = []
    for company, symbol in COMPANIES.items():
        logging.info(f"Fetching data for {company} ({symbol})...")
        data = fetch_data(symbol)
        if data is not None:
            all_data.append(data)
        """Due to API rate limits"""
        time.sleep(15)  

    if all_data:
        df_all = pd.concat(all_data)
        save_to_csv_and_db(df_all, OUTPUT_FILE, engine)
    else:
        logging.error("No data fetched.")

if __name__ == "__main__":
    main()
