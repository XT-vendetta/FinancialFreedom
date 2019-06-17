import MySQLdb
import pandas as pd


def read_stocks(ts_codes):
    db = MySQLdb.connect("localhost", "root", "password", "stock", charset='utf8')
    code_price_dict = dict()
    for ts_code in ts_codes:
        sql = "SELECT * FROM stock WHERE ts_code='" + ts_code + "';"
        df = pd.read_sql(sql, con=db)
        code_price_dict[ts_code] = df
    db.close()
    return code_price_dict


if __name__ == "__main__":
    print read_stocks(['000001.SZ'])['000001.SZ']