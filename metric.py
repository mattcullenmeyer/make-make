import api
import helper

# Get existing data from Digital Ocean
metadata = api.get('metadata')
metric = api.get('metric')

data = metadata.merge(
    metric,
    left_on='ticker',
    right_on='ticker',
    suffixes=(None, '_x')
)

data = data.fillna('')

for i in data.index:

    # Print progress
    print(f'#{i + 1} {helper.progress(i + 1, data.index)}')

    tmp = data.loc[i]

    ticker = tmp.ticker
    sector = tmp.sector
    industry = tmp.industry

    sec = data[data.sector == sector]
    ind = data[data.industry == industry]

    col = 'pe_value'
    pe_sec_median, pe_sec_rank, pe_ind_median, pe_ind_rank = (
        helper.all_rank(tmp[col], sec[col], ind[col]))

    col = 'pb_value'
    pb_sec_median, pb_sec_rank, pb_ind_median, pb_ind_rank = (
        helper.all_rank(tmp[col], sec[col], ind[col]))

    col = 'ps_value'
    ps_sec_median, ps_sec_rank, ps_ind_median, ps_ind_rank = (
        helper.all_rank(tmp[col], sec[col], ind[col]))

    col = 'pcf_value'
    pcf_sec_median, pcf_sec_rank, pcf_ind_median, pcf_ind_rank = (
        helper.all_rank(tmp[col], sec[col], ind[col]))

    col = 'eve_value'
    eve_sec_median, eve_sec_rank, eve_ind_median, eve_ind_rank = (
        helper.all_rank(tmp[col], sec[col], ind[col]))

    value_avg = helper.mean([pe_sec_rank, pb_sec_rank, ps_sec_rank,
                             pcf_sec_rank, eve_sec_rank])

    col = 'mom_12_value'
    mom_12_sec_median, mom_12_sec_rank, mom_12_ind_median, mom_12_ind_rank = (
        helper.all_rank(tmp[col], sec[col], ind[col]))

    col = 'mom_6_value'
    mom_6_sec_median, mom_6_sec_rank, mom_6_ind_median, mom_6_ind_rank = (
        helper.all_rank(tmp[col], sec[col], ind[col]))

    # mom_avg = helper.mean([mom_12_sec_rank, mom_6_sec_rank])
    mom_avg = mom_12_sec_rank

    col = 'vol_12_value'
    vol_12_sec_median, vol_12_sec_rank, vol_12_ind_median, vol_12_ind_rank = (
        helper.all_inv(tmp[col], sec[col], ind[col]))

    col = 'beta_value'
    beta_sec_median, beta_sec_rank, beta_ind_median, beta_ind_rank = (
        helper.all_inv(tmp[col], sec[col], ind[col]))

    # vol_avg = helper.mean([vol_12_sec_rank, beta_sec_rank])
    vol_avg = vol_12_sec_rank

    col = 'asset_turn_value'
    (asset_turn_sec_median, asset_turn_sec_rank, asset_turn_ind_median,
     asset_turn_ind_rank) = helper.all_rank(tmp[col], sec[col], ind[col])

    col = 'gross_profit_value'
    (gross_profit_sec_median, gross_profit_sec_rank, gross_profit_ind_median,
     gross_profit_ind_rank) = helper.all_rank(tmp[col], sec[col], ind[col])

    col = 'gross_margin_value'
    (gross_margin_sec_median, gross_margin_sec_rank, gross_margin_ind_median,
     gross_margin_ind_rank) = helper.all_rank(tmp[col], sec[col], ind[col])

    col = 'return_asset_value'
    (return_asset_sec_median, return_asset_sec_rank, return_asset_ind_median,
     return_asset_ind_rank) = helper.all_rank(tmp[col], sec[col], ind[col])

    profit_avg = helper.mean([asset_turn_sec_rank, gross_profit_sec_rank,
                              gross_margin_sec_rank, return_asset_sec_rank])

    col = 'ext_fin_value'
    (ext_fin_sec_median, ext_fin_sec_rank, ext_fin_ind_median,
     ext_fin_ind_rank) = helper.all_inv(tmp[col], sec[col], ind[col])

    col = 'cf_debt_value'
    (cf_debt_sec_median, cf_debt_sec_rank, cf_debt_ind_median,
     cf_debt_ind_rank) = helper.all_rank(tmp[col], sec[col], ind[col])

    finance_avg = helper.mean([ext_fin_sec_rank, cf_debt_sec_rank])

    col = 'accrual_value'
    (accrual_sec_median, accrual_sec_rank, accrual_ind_median,
     accrual_ind_rank) = helper.all_inv(tmp[col], sec[col], ind[col])

    safety_avg = accrual_sec_rank

    quality_avg = helper.mean([vol_avg, profit_avg, finance_avg, safety_avg])
    overall_avg = helper.mean([value_avg, mom_avg, quality_avg])

    metric_data = {
        'ticker': f'{ticker}',
        'pe_sec_median': f'{helper.num_str(pe_sec_median, 3)}',
        'pe_sec_rank': f'{helper.num_str(pe_sec_rank, 0)}',
        'pe_ind_median': f'{helper.num_str(pe_ind_median, 3)}',
        'pe_ind_rank': f'{helper.num_str(pe_ind_rank, 0)}',
        'pb_sec_median': f'{helper.num_str(pb_sec_median, 3)}',
        'pb_sec_rank': f'{helper.num_str(pb_sec_rank, 0)}',
        'pb_ind_median': f'{helper.num_str(pb_ind_median, 3)}',
        'pb_ind_rank': f'{helper.num_str(pb_ind_rank, 0)}',
        'ps_sec_median': f'{helper.num_str(ps_sec_median, 3)}',
        'ps_sec_rank': f'{helper.num_str(ps_sec_rank, 0)}',
        'ps_ind_median': f'{helper.num_str(ps_ind_median, 3)}',
        'ps_ind_rank': f'{helper.num_str(ps_ind_rank, 0)}',
        'pcf_sec_median': f'{helper.num_str(pcf_sec_median, 3)}',
        'pcf_sec_rank': f'{helper.num_str(pcf_sec_rank, 0)}',
        'pcf_ind_median': f'{helper.num_str(pcf_ind_median, 3)}',
        'pcf_ind_rank': f'{helper.num_str(pcf_ind_rank, 0)}',
        'eve_sec_median': f'{helper.num_str(eve_sec_median, 3)}',
        'eve_sec_rank': f'{helper.num_str(eve_sec_rank, 0)}',
        'eve_ind_median': f'{helper.num_str(eve_ind_median, 3)}',
        'eve_ind_rank': f'{helper.num_str(eve_ind_rank, 0)}',
        'mom_12_sec_median': f'{helper.num_str(mom_12_sec_median, 3)}',
        'mom_12_sec_rank': f'{helper.num_str(mom_12_sec_rank, 0)}',
        'mom_12_ind_median': f'{helper.num_str(mom_12_ind_median, 3)}',
        'mom_12_ind_rank': f'{helper.num_str(mom_12_ind_rank, 0)}',
        'mom_6_sec_median': f'{helper.num_str(mom_6_sec_median, 3)}',
        'mom_6_sec_rank': f'{helper.num_str(mom_6_sec_rank, 0)}',
        'mom_6_ind_median': f'{helper.num_str(mom_6_ind_median, 3)}',
        'mom_6_ind_rank': f'{helper.num_str(mom_6_ind_rank, 0)}',
        'vol_12_sec_median': f'{helper.num_str(vol_12_sec_median, 3)}',
        'vol_12_sec_rank': f'{helper.num_str(vol_12_sec_rank, 0)}',
        'vol_12_ind_median': f'{helper.num_str(vol_12_ind_median, 3)}',
        'vol_12_ind_rank': f'{helper.num_str(vol_12_ind_rank, 0)}',
        'beta_sec_median': f'{helper.num_str(beta_sec_median, 3)}',
        'beta_sec_rank': f'{helper.num_str(beta_sec_rank, 0)}',
        'beta_ind_median': f'{helper.num_str(beta_ind_median, 3)}',
        'beta_ind_rank': f'{helper.num_str(beta_ind_rank, 0)}',
        'asset_turn_sec_median': f'{helper.num_str(asset_turn_sec_median, 3)}',
        'asset_turn_sec_rank': f'{helper.num_str(asset_turn_sec_rank, 0)}',
        'asset_turn_ind_median': f'{helper.num_str(asset_turn_ind_median, 3)}',
        'asset_turn_ind_rank': f'{helper.num_str(asset_turn_ind_rank, 0)}',
        'gross_profit_sec_median': f'{helper.num_str(gross_profit_sec_median, 3)}',
        'gross_profit_sec_rank': f'{helper.num_str(gross_profit_sec_rank, 0)}',
        'gross_profit_ind_median': f'{helper.num_str(gross_profit_ind_median, 3)}',
        'gross_profit_ind_rank': f'{helper.num_str(gross_profit_ind_rank, 0)}',
        'gross_margin_sec_median': f'{helper.num_str(gross_margin_sec_median, 3)}',
        'gross_margin_sec_rank': f'{helper.num_str(gross_margin_sec_rank, 0)}',
        'gross_margin_ind_median': f'{helper.num_str(gross_margin_ind_median, 3)}',
        'gross_margin_ind_rank': f'{helper.num_str(gross_margin_ind_rank, 0)}',
        'return_asset_sec_median': f'{helper.num_str(return_asset_sec_median, 3)}',
        'return_asset_sec_rank': f'{helper.num_str(return_asset_sec_rank, 0)}',
        'return_asset_ind_median': f'{helper.num_str(return_asset_ind_median, 3)}',
        'return_asset_ind_rank': f'{helper.num_str(return_asset_ind_rank, 0)}',
        'ext_fin_sec_median': f'{helper.num_str(ext_fin_sec_median, 3)}',
        'ext_fin_sec_rank': f'{helper.num_str(ext_fin_sec_rank, 0)}',
        'ext_fin_ind_median': f'{helper.num_str(ext_fin_ind_median, 3)}',
        'ext_fin_ind_rank': f'{helper.num_str(ext_fin_ind_rank, 0)}',
        'cf_debt_sec_median': f'{helper.num_str(cf_debt_sec_median, 3)}',
        'cf_debt_sec_rank': f'{helper.num_str(cf_debt_sec_rank, 0)}',
        'cf_debt_ind_median': f'{helper.num_str(cf_debt_ind_median, 3)}',
        'cf_debt_ind_rank': f'{helper.num_str(cf_debt_ind_rank, 0)}',
        'accrual_sec_median': f'{helper.num_str(accrual_sec_median, 3)}',
        'accrual_sec_rank': f'{helper.num_str(accrual_sec_rank, 0)}',
        'accrual_ind_median': f'{helper.num_str(accrual_ind_median, 3)}',
        'accrual_ind_rank': f'{helper.num_str(accrual_ind_rank, 0)}',
        'value_avg': f'{helper.num_str(value_avg, 3)}',
        'mom_avg': f'{helper.num_str(mom_avg, 3)}',
        'vol_avg': f'{helper.num_str(vol_avg, 3)}',
        'profit_avg': f'{helper.num_str(profit_avg, 3)}',
        'finance_avg': f'{helper.num_str(finance_avg, 3)}',
        'safety_avg': f'{helper.num_str(safety_avg, 3)}',
        'quality_avg': f'{helper.num_str(quality_avg, 3)}',
        'composite_avg': f'{helper.num_str(overall_avg, 3)}'
    }

    # Update metric table in Digital Ocean
    if ticker in metric.ticker.values:
        r = api.put('metric', ticker, metric_data)
        if r.status_code != 200:
            print('Something went wrong with metric request')
            break
    else:
        r = api.post('metric', metric_data)
        if r.status_code != 201:
            print('Something went wrong with metric request')
            break
