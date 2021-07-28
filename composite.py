import api
import helper


# Get existing data from Digital Ocean
metadata = api.get('metadata')
metric = api.get('metric')

data = metadata.merge(metric, 
    left_on='ticker', right_on='ticker', suffixes=(None, '_x'))

data = data.fillna('')

for i in data.index:
    
    # Print progress
    print(f'#{i+1} {helper.progress(i+1, data.index)}')
    
    tmp = data.loc[i]
    
    ticker = tmp.ticker
    sector = tmp.sector

    sec = data[data.sector == sector]

    col = 'value_avg'
    value_rank = helper.ranking(tmp[col], sec[col])
    col = 'mom_avg'
    mom_rank = helper.ranking(tmp[col], sec[col])
    col = 'profit_avg'
    vol_rank = helper.ranking(tmp[col], sec[col])
    col = 'profit_avg'
    profit_rank = helper.ranking(tmp[col], sec[col])
    col = 'finance_avg'
    finance_rank = helper.ranking(tmp[col], sec[col])
    col = 'safety_avg'
    safety_rank = helper.ranking(tmp[col], sec[col])
    col = 'quality_avg'
    quality_rank = helper.ranking(tmp[col], sec[col])
    col = 'composite_avg'
    composite_rank = helper.ranking(tmp[col], sec[col])


    metadata_data = {
        'ticker': f'{ticker}',
        'value_rank': f'{helper.num_str(value_rank, 0)}',
        'mom_rank': f'{helper.num_str(mom_rank, 0)}',
        'vol_rank': f'{helper.num_str(vol_rank, 0)}',
        'profit_rank': f'{helper.num_str(profit_rank, 0)}',
        'finance_rank': f'{helper.num_str(finance_rank, 0)}',
        'safety_rank': f'{helper.num_str(safety_rank, 0)}',
        'quality_rank': f'{helper.num_str(quality_rank, 0)}',
        'composite_rank': f'{helper.num_str(composite_rank, 0)}'
    }
    
    # Update metadata table in Digial Ocean
    if ticker in metadata.ticker.values:
        r = api.put('metadata', ticker, metadata_data)
        if r.status_code != 200:
            print('Something went wrong with metadata request')
            break
    else:
        r = api.post('metadata', metadata_data)
        if r.status_code != 201:
            print('Something went wrong with metadata request')
            break