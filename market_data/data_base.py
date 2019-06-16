import MySQLdb
from query import *

db = MySQLdb.connect("localhost", "root", "password", "stock", charset='utf8')
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data

stock_list = list(get_stock_list()['ts_code'])

for stock in stock_list:
    print "Updating " + stock + " ..."
    df = get_stock_daily_data(stock, '20170101', '20190614')
    for row in df.iterrows():
        key, value = row
        value_parsed = []
        for s in list(value):
            if type(s) is unicode:
                value_parsed.append("'" + s + "'")
            else:
                value_parsed.append(str(s))

        sql = """INSERT INTO STOCK(ts_code, trade_date, open, high, low, close,
        pre_close, chg, pct_chg, vol, amount)
        VALUES(""" + ','.join(value_parsed) + ')'
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            raise
    print "Done updating " + stock + " ..."
db.close()