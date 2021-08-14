import numpy as np

import _api as api
import _helper as helper
import _scraper as scraper


# Get existing data from Digital Ocean
tickers = api.get('ticker')
sectors = api.get('sector')
industries = api.get('industry')
market_caps = api.get('size')
liquidities = api.get('liquidity')
metadata = api.get('metadata')
metrics = api.get('metric')

# Generate list of ticker symbols
ticker_symbols = tickers.ticker.values
ticker_symbols.sort()
# ticker_symbols = ticker_symbols[:5]

cnt = 0
for ticker in ticker_symbols:
    
    # Print progress
    cnt += 1
    print(f'{ticker} #{cnt} {helper.progress(cnt, ticker_symbols)}')
    
    # ticker_id = tickers[tickers.ticker == ticker].id.values[0]
    
    print('\tIncome Statement')
    # Get Income Statement from Stockrow
    inc_stmt = scraper.get_stockrow(ticker, 'is')
    helper.wait()
    
    print('\tYahoo Finance')
    # Get data from Yahoo Finance
    yahoo = scraper.get_yahoo(ticker)
    helper.wait()
    
    print('\tBalance Sheet')
    # Get Balance Sheet from Stockrow
    bal_sheet = scraper.get_stockrow(ticker, 'bs')
    helper.wait()
    
    print('\tPrices')
    # Get historical prices
    prices = scraper.get_prices(ticker, 400)
    helper.wait()
    
    print('\tCash Flow')
    # Get Cash Flow from Stockrow
    cf_stmt = scraper.get_stockrow(ticker, 'cf')
    helper.wait()

    ''' METADATA '''
    
    # price / earnings
    price = helper.yahoo_number(yahoo, 'financialData', 'currentPrice')
    eps = helper.yahoo_number(yahoo, 'defaultKeyStatistics', 'trailingEps')
    pe = np.nan
    if abs(eps) != 0:
        pe = price / eps
    pe_value = 1 / pe
        
    # price / book
    book = helper.yahoo_number(yahoo, 'defaultKeyStatistics', 'bookValue')
    pb = price / book
    pb_value = 1 / pb
    
    # price / sales
    ps = helper.yahoo_number(yahoo, 'summaryDetail', 'priceToSalesTrailing12Months')
    ps_value = 1 / ps
    
    # price / ocf
    ocf = helper.yahoo_number(yahoo, 'financialData', 'operatingCashflow')
    shares = helper.yahoo_number(yahoo, 'defaultKeyStatistics', 'sharesOutstanding')
    pcf = np.nan
    if shares != 0 and ocf != 0:
        pcf = price / (ocf / shares)
    pcf_value = 1 / pcf
    
    # ev / ebtida
    ev_ebitda = helper.yahoo_number(yahoo, 'defaultKeyStatistics', 'enterpriseToEbitda')
    eve_value = np.nan
    if ev_ebitda != 0:
        eve_value = 1 / ev_ebitda
    
    # beta
    beta_value = helper.yahoo_number(yahoo, 'summaryDetail', 'beta')
    
    # 52 week range
    fiftyTwoWeekHigh = helper.yahoo_number(yahoo, 'summaryDetail', 'fiftyTwoWeekHigh')
    fiftyTwoWeekLow = helper.yahoo_number(yahoo, 'summaryDetail', 'fiftyTwoWeekLow')
    
    # bid / ask
    bid = helper.yahoo_number(yahoo, 'summaryDetail', 'bid')
    ask = helper.yahoo_number(yahoo, 'summaryDetail', 'ask')
    
    # volume
    volume = helper.yahoo_number(yahoo, 'summaryDetail', 'volume')
    avg_volume = helper.yahoo_number(yahoo, 'summaryDetail', 'averageVolume')
    
    # metadata
    sector = helper.yahoo_text(yahoo, 'summaryProfile', 'sector')
    industry = helper.yahoo_text(yahoo, 'summaryProfile', 'industry')
    market_cap = helper.yahoo_number(yahoo, 'summaryDetail', 'marketCap')
    # company_name = yahoo['price']['longName'].replace("'","''")
    company_name = helper.yahoo_text(yahoo, 'price', 'longName').replace("'", "''")
    company_name_ticker = company_name + ' (' + ticker + ')'

    # check for new industry
    if len(industries[industries.industry == industry]) == 0:
        if industry != 'None' and industry != '':
            # add new industry to industries
            data = {'industry': f'{industry}'}
            api.post('industry', data)
            # get updated industries
            industries = api.get('industry')

    # find metadata IDs
    if sector != '':
        clean_sector = helper.map_sectors(sector, sectors)
        sector_id = sectors[sectors.sector == clean_sector].id.values[0]
    else:
        sector_id = ''
    
    if industry != 'None' and industry != '':
        industry_id = industries[industries.industry == industry].id.values[0]
    else:
        industry_id = ''
    
    size_id = helper.find_size(market_cap)
    liquidity_id = helper.find_liquidity(avg_volume)

    last_updated = ''
    if not prices.empty:
        last_updated = prices.loc[0, 'date']

    # Update ticker table in Digital Ocean
    ticker_data = {
         'ticker': f'{ticker}',
        'company_name_ticker': f'{company_name_ticker}'   
    }

    # api currently can't handle periods in slug
    if ticker.find('.') == -1:
        r = api.put('ticker', ticker, ticker_data)
        if r.status_code != 200:
            print('Something went wrong with ticker request')
            break
    
    if ticker.find('.') == -1:
        ticker_id = api.get('ticker', ticker).loc[0, 'id']
    else:
        tmp = api.get('ticker')
        ticker_id = tmp[tmp.ticker == ticker].id.values[0]

    # prepare to put or post data to Digital Ocean
    metadata_data = {
        'ticker': f'{ticker_id}',
        'sector': f'{sector_id}',
        'industry': f'{industry_id}',
        'market_cap_size': f'{size_id}',
        'liquidity': f'{liquidity_id}',
        'price': f'{helper.num_str(price, 2)}',
        'fiftyTwoWeekHigh': f'{helper.num_str(fiftyTwoWeekHigh, 2)}',
        'fiftyTwoWeekLow': f'{helper.num_str(fiftyTwoWeekLow, 2)}',
        'bid': f'{helper.num_str(bid, 2)}',
        'ask': f'{helper.num_str(ask, 2)}',
        'volume': f'{helper.num_str(volume, 0)}',
        'avg_volume': f'{helper.num_str(avg_volume, 0)}',
        'market_cap': f'{helper.num_str(market_cap, 0)}',
        'company_name': f'{company_name}',
        'last_updated': f'{last_updated}'
    }

    # Update metadata table in Digial Ocean
    if ticker_id in metadata.ticker.values:
        r = api.put('metadata', ticker_id, metadata_data)
        if r.status_code != 200:
            print('Something went wrong with metadata request')
            break
    else:
        r = api.post('metadata', metadata_data)
        if r.status_code != 201:
            print('Something went wrong with metadata request')
            break

    ''' METRICS '''
    
    # Momentum
    # 252 trading days in year; 126 in half year
    # due to zero-based indexing, subtract 1
    mom_12_value = helper.mom_calc(prices, 252-1)
    mom_6_value = helper.mom_calc(prices, 126-1)
    
    # Volatility
    vol_12_value = helper.vol_calc(prices, 252)

    # Fundamentals
    total_revenue = helper.read_is('Revenue', inc_stmt)
    total_assets = helper.read_bs('Total Assets', bal_sheet)
    gross_profit = helper.read_is('Gross Profit', inc_stmt)
    op_income = helper.read_is('Income from Continuous Operations', inc_stmt)
    fin_cf = helper.read_is('Financing cash flow', cf_stmt)
    net_inc = helper.read_is('Consolidated Net Income/Loss', inc_stmt)
    op_cf = helper.read_is('Operating Cash Flow', cf_stmt)
    cash = helper.read_bs('Cash and Short Term Investments', bal_sheet)
    net_debt = helper.read_bs('Net Debt', bal_sheet)
        
    total_debt = net_debt + cash
    
    if total_revenue != 0:
        
        if total_assets != 0:
            # total asset turnover
            asset_turn_value = total_revenue / total_assets
        else:
            asset_turn_value = np.nan
            
        if gross_profit != 0:
            # gross profit margin
            gross_margin_value = gross_profit / total_revenue
        else:
            gross_margin_value = np.nan
    
    else:
        asset_turn_value = np.nan
        gross_margin_value = np.nan

    if total_assets != 0:
        
        if gross_profit != 0:
            # gross profitability
            gross_profit_value = gross_profit / total_assets
        else:
            gross_profit_value = np.nan
        
        if op_income != 0:
            # return on assets (excl extraordinary items)
            return_asset_value = op_income / total_assets
        else:
            return_asset_value = np.nan

        if fin_cf != 0:
            # external financing
            ext_fin_value = fin_cf / total_assets
        else:
            ext_fin_value = np.nan
        
    else:
        gross_profit_value = np.nan
        return_asset_value = np.nan
        ext_fin_value = np.nan

    if op_cf != 0:
        
        if total_debt != 0:
            # cash flow-to-debt
            cf_debt_value = op_cf / total_debt
        else:
            cf_debt_value = np.nan
        
        if net_inc != 0 and total_assets != 0:
            # accruals-to-assets
            accrual_value = (net_inc - op_cf) / total_assets
        else:
            accrual_value = np.nan
            
    else:
        cf_debt_value = np.nan
        accrual_value = np.nan

    metric_data = {
        'ticker': f'{ticker_id}',
        'pe_value': f'{helper.num_str(pe_value)}',
        'pb_value': f'{helper.num_str(pb_value)}',
        'ps_value': f'{helper.num_str(ps_value)}',
        'pcf_value': f'{helper.num_str(pcf_value)}',
        'eve_value': f'{helper.num_str(eve_value)}',
        'mom_12_value': f'{helper.num_str(mom_12_value)}',
        'mom_6_value': f'{helper.num_str(mom_6_value)}',
        'vol_12_value': f'{helper.num_str(vol_12_value)}',
        'beta_value': f'{helper.num_str(beta_value)}',
        'asset_turn_value': f'{helper.num_str(asset_turn_value)}',
        'gross_profit_value': f'{helper.num_str(gross_profit_value)}',
        'gross_margin_value': f'{helper.num_str(gross_margin_value)}',
        'return_asset_value': f'{helper.num_str(return_asset_value)}',
        'ext_fin_value': f'{helper.num_str(ext_fin_value)}',
        'cf_debt_value': f'{helper.num_str(cf_debt_value)}',
        'accrual_value': f'{helper.num_str(accrual_value)}'
    }    

    # Update metric table in Digital Ocean
    if ticker_id in metrics.ticker.values:
        r = api.put('metric', ticker_id, metric_data)
        if r.status_code != 200:
            print('Something went wrong with metric request')
            break
    else:
        r = api.post('metric', metric_data)
        if r.status_code != 201:
            print('Something went wrong with metric request')
            break
