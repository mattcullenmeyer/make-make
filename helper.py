import numpy as np
import time
import random
from scipy import stats


# Function to wait between requests
def wait(seconds=2):
    time.sleep(random.random() * seconds + seconds)


# Function to determine percentage complete
def progress(cnt, values):
    fraction = (cnt - 1) / len(values)
    return f'{np.round(fraction * 100, 1)}%'


def map_sectors(sector, sectors):
    if sector in sectors.sector.values:
        return sector
    
    sector_map = {
        'Industrial Goods': 'Industrials'    
    }
    
    return sector_map[sector]
    

# Function for determining market cap size id
def find_size(cap):
    # exclude mega >200B b/c there's only 21 stocks

    # large >10B
    if cap > 10e9:
        return 1
    # mid 2B-10B
    elif cap >= 2e9:
        return 2
    # small 300M-2B
    elif cap >= 300e6:
        return 3
    # micro 50M-300M
    elif cap >= 50e6:
        return 4
    # nano <50M
    else:
        return 5


# Function for determining liquidity id
def find_liquidity(volume):
    return ''


# Function for calculating momentum
def mom_calc(prices, n):
    if len(prices.index) > n:
        if prices.loc[n, 'close'] != 0:
            return (prices.loc[0, 'close'] /
                prices.loc[n, 'close'] - 1)
        else:
            return np.nan
    else:
        return np.nan


# Function for calculating volatility
def vol_calc(prices, n):
    if len(prices.index) > n:
        prices['price_return'] = prices.close / prices.close.shift(-1) - 1
        daily_vol = prices.loc[:n-1, 'price_return'].std()
        vol_12_value = daily_vol * np.sqrt(n)
        return vol_12_value
    
    return np.nan


# Convert Yahoo field to number
def yahoo_number(yahoo, col1, col2):
    try:
        num = yahoo[col1][col2]
        if num != {}:
            return float(num['raw'])
        else:
            return np.nan
    except KeyError:
        return np.nan
    

def yahoo_text(yahoo, col1, col2):
    try:
        text = yahoo[col1][col2]
        return text
    except KeyError:
        return ''
    

# function for Digital Ocean values upload
def num_str(value, n=5):
    if str(value) in ('', 'nan', 'inf', '-inf'):
        return ''
    else:
        return str(np.round(value, n))


# Function to determine if line item exists in balance sheet
def read_bs(name, data):
    if name in data.index:
        return data.loc[name][0]
    else:
        return 0
    
    
# Function to determine if line item exists in income stmt or cash flow stmt
def read_is(name, data):
    if name in data.index:
        return data.loc[name].sum()
    else:
        return 0
    

# remove nulls from list of values
def float_values(values):
    return [value for value in values.values if value != '']


# function for median
def median(data):
    values = float_values(data)
    if len(values) > 0:
        return np.nanpercentile(values, 50)
    else:
        return np.nan


# function for standard ranking
def ranking(value, data):
    values = float_values(data)
    if value != '':
        if np.abs(value) > 0:
            return stats.percentileofscore(values, value)
        else:
            return np.nan
    else:
        return np.nan


# function for inverse ranking
def inverse(value, data):
    values = float_values(data)
    if value != '':
        if np.abs(value) > 0:
            return 100 - stats.percentileofscore(values, value)
        else:
            return np.nan
    else:
        return np.nan


# function to return mean
def mean(values):
    clean_values = [value for value in values if not np.isnan(value)]

    if len(clean_values) > 0:
        return np.mean(clean_values)
    else:
        return np.nan
    
def all_rank(value, sec, ind):
    return (
        median(sec),
        ranking(value, sec),
        median(ind),
        ranking(value, ind)
    )

def all_inv(value, sec, ind):
    return (
        median(sec),
        inverse(value, sec),
        median(ind),
        inverse(value, ind)
    )