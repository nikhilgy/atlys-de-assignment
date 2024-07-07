import requests
import pandas as pd
import logging
from sqlalchemy import create_engine
from datetime import datetime
from config import ALPHA_VANTAGE_API_KEY, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    filemode='a',
    format='%(asctime)s: %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

COMPANIES = {
    "RELIANCE": "RELIANCE.BSE"
    # "TCS": "TCS.BSE",
    # "HDFCBANK": "HDFCBANK.BSE",
    # "ICICIBANK": "ICICIBANK.BSE",
    # "BHARTIARTL": "BHARTIARTL.BSE",
    # "SBIN": "SBIN.BSE",
    # "INFY": "INFY.BSE",
    # "LIC": "LICI.BSE",
    # "HINDUNILVR": "HINDUNILVR.BSE",
    # "ITC": "ITC.BSE"
}

BASE_URL = "https://www.alphavantage.co/query"

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

def fetch_data(symbol, start_date=None, end_date=None):
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
        logging.info("Dataframe: {}".format(df))
        if start_date and end_date:
            df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        elif start_date:
            df = df[df['Date'] == start_date]

        return df
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error for {symbol}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error for {symbol}: {e}")
        return None

def save_to_db(dataframe, table_name='historical_stock_prices'):
    try:
        dataframe.to_sql(table_name, engine, if_exists='append', index=False)
        logging.info(f"Data saved to database.")
    except Exception as e:
        logging.error(f"Error saving data to database: {e}")
