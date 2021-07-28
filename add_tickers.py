import pandas as pd
import time

import api
import helper

# go to https://www.zacks.com/screening/stock-screener
''' 
### Screen Criteria ###
Market Cap > 0 # you need to have at least 1 criteria
### Edit View ###
# these are found under Company Description
Exchange
COM/ADR/Canadian 
'''

# Get existing data from Digital Ocean
tickers = api.get('ticker')

exchanges = ['OTC', 'OTCBB']
types = ['COM', 'MLP']

# upload the full list of tickers from Zacks
file_path = 'C:/Users/mattc/Custom Scripts/TinyTrader Scraping/'
data = pd.read_csv(file_path + 'zacks.csv')

# Change TRUE ticker from boolean to string
data['Ticker'].replace(True, 'TRUE', inplace=True)

new_data = data[
	(data['Market Cap (mil)'] >= 50)
	& (~data['Exchange'].isin(exchanges))
	& (data['COM/ADR/Canadian'].isin(types))]

# list of current tickers
new_tickers = list(new_data.Ticker.values)

# list of existing tickers
old_tickers = list(tickers.ticker.values)

# add ticker_symbols
add_tickers = [ticker for ticker in new_tickers
	if ticker not in old_tickers]

# delete ticker_symbols
delete_tickers = [ticker for ticker in old_tickers 
	if ticker not in new_tickers]

print(f'\nAdding {len(add_tickers)} tickers\n')
print(f'\nDeleting {len(delete_tickers)} tickers\n')

input("Press Enter to continue...")

cnt = 0
for ticker in add_tickers:
    
    # Print progress
    cnt += 1
    print(f'{ticker} #{cnt} {helper.progress(cnt, add_tickers)}')
    
    time.sleep(0.5)
    ticker_data = {
        'ticker': f'{ticker}',
        'company_name_ticker': ''
    }
    r = api.post('ticker', ticker_data)
    if r.status_code != 201:
        print('Something went wrong with adding ticker')
        break
'''
for ticker in delete_tickers:
    r = api.delete('ticker', ticker)
    if r.status_code != 204:
        print('Something went wrong with deleting ticker')
        break
'''