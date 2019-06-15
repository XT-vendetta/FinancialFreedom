import tushare

tushare.set_token("d1535cca717de08e93f747b7a266b613e4062c45443e43a557da5f66")
pro = tushare.pro_api("d1535cca717de08e93f747b7a266b613e4062c45443e43a557da5f66")


def get_stock_list():
    stock_list = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    return stock_list


def get_stock_daily_data1():
    df = tushare.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20180101', end_date='20181011')
    return df


def get_stock_daily_data(ts_code, start_date, end_date):
    df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
    return df


if __name__ == "__main__":
    print get_stock_daily_data('000001.SZ', '20190101', '20190614')