import tushare as ts

pro = ts.pro_api("d1535cca717de08e93f747b7a266b613e4062c45443e43a557da5f66")

data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

print data