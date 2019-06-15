import market_data
from numpy import zeros, array
from pandas import DataFrame


def accumulative_return(daily_df, n):
    day_len = len(daily_df.index)
    dates = list(daily_df['trade_date'])[0:day_len - n + 1]
    assert day_len >= n
    pct_chg = array(df['pct_chg'])
    return_val = zeros(day_len - n + 1)
    for i in range(0, n):
        return_val = return_val + pct_chg[i: day_len - n + 1 + i]
    return DataFrame({'ACCUM_RETURN' : return_val}, index=dates)


if __name__ == "__main__":
    df = market_data.get_stock_daily_data('000001.SZ', '20190101', '20190614')
    codes = list(market_data.get_stock_list()['ts_code'])
    for code in codes:
        df = market_data.get_stock_daily_data(code, '20190101', '20190614')
        accum_return = None
        try:
            accum_return = accumulative_return(df, 3)
        except Exception, e:
            print code
        dates = accum_return.index[accum_return['ACCUM_RETURN'] > 28].tolist()
        for date in dates:
            print code + "\t" + date
