import requests
import pandas as pd
from yahoofinancials import YahooFinancials
from datetime import date, timedelta
import time


def adjust_ticker(ticker):
    return ticker.replace('.', '-')


def get_yahoo(ticker):
    adj_ticker = adjust_ticker(ticker)

    url = (
        'https://query2.finance.yahoo.com/v10/finance/'
        f'quoteSummary/{adj_ticker}?formatted=true&lang='
        'en-US&region=US&modules='
        'summaryProfile%2C'
        'financialData%2C'
        'defaultKeyStatistics%2C'
        'summaryDetail%2C'
        'price'
        '&corsDomain=finance.yahoo.com'
    )

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }

    attempt = 0;
    success = False
    while attempt < 2 and success == False:
        try:
            r = requests.get(url, headers=headers, timeout=5)
            success = True
        except:
            time.sleep(10)
            attempt += 1

    if success == True:
        data = r.json()

        result = data['quoteSummary']['result']

        if result:
            return result[0]
        return {}

    return {}


def get_prices(ticker, days):
    adj_ticker = adjust_ticker(ticker)

    # Set date range for historical prices
    end = date.today()
    start = end - timedelta(days)  # only need 1 year
    # (5*365) for 5 years if calculating beta
    end = end.strftime('%Y-%m-%d')
    start = start.strftime('%Y-%m-%d')

    json_prices = YahooFinancials(adj_ticker).get_historical_price_data(
        start, end, 'daily')

    if 'prices' in json_prices[adj_ticker].keys():
        raw_prices = pd.DataFrame(json_prices[adj_ticker]['prices'])[
            ['formatted_date', 'close', 'volume']]
        raw_prices.rename(columns={'formatted_date': 'date'}, inplace=True)
        raw_prices = raw_prices.iloc[::-1]
        raw_prices.reset_index(inplace=True)
        raw_prices.bfill(inplace=True)
        prices = raw_prices[['date', 'close', 'volume']]

        return prices

    return pd.DataFrame()


def get_stockrow(ticker, stmt):
    stmts = {
        'is': 'Income%20Statement',
        'bs': 'Balance%20Sheet',
        'cf': 'Cash%20Flow'
    }

    url = (
        f'https://stockrow.com/api/companies/{ticker}'
        f'/financials.xlsx?dimension=Q&section={stmts[stmt]}'
    )

    attempt = 0;
    success = False
    while attempt < 2 and success == False:
        try:
            raw_data = pd.read_excel(url, index_col=0)
            data = raw_data[raw_data.columns[:4]]
            return data
        except:
            time.sleep(10)
            attempt += 1

    return pd.DataFrame()
