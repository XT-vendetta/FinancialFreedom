import time
from market_data.query import get_stock_list
from market_data.read_database import read_stocks
from sklearn import svm, linear_model
import matplotlib.pyplot as plt
from pandas import DataFrame

ts_codes = list(get_stock_list()['ts_code'])
#ts_codes = ['000001.SZ']

train_codes = []
test_codes = []

count = 0
for ts_code in ts_codes:
    if count % 2 == 0:
        train_codes.append(ts_code)
    else:
        test_codes.append(ts_code)
    count += 1

start_time = time.time()
print "Start reading stock data... "
fit_data_dict = read_stocks(ts_codes)
end_time = time.time()
print "Read stock data uses " + str(end_time - start_time) + "s."

train_days = 100
test_days = 5
total_days = train_days + test_days

x_train = []
y_train = []

x_test = []
y_test = []

test_codes_actual = []

use_pct_chg = True
use_vol = False
use_amount = False

for ts_code in ts_codes:
    stock_df = fit_data_dict[ts_code]
    if len(stock_df.index) < total_days:
        continue
    stock_df.sort_values(by=['trade_date'])
    x_i = []
    if use_pct_chg:
        x_i = x_i + list(stock_df['pct_chg'])[-total_days:-test_days]
    if use_vol:
        x_i = x_i + list(stock_df['vol'])[-total_days:-test_days]
    if use_amount:
        x_i = x_i + list(stock_df['amount'])[-total_days:-test_days]
    y_i = sum(list(stock_df['pct_chg'])[-test_days:])

    if ts_code in train_codes:
        x_train.append(x_i)
        y_train.append(y_i)
    else:
        x_test.append(x_i)
        y_test.append(y_i)
        test_codes_actual.append(ts_code)


start_time = time.time()

#clf = svm.SVR()
clf = linear_model.Lasso(alpha=0.01, max_iter=10000)
clf.fit(x_train, y_train)

end_time = time.time()
print "Fit data uses " + str(end_time - start_time) + "s."

y_test_est = clf.predict(x_test)

result_df = DataFrame({'ACTUAL' : y_test, 'ESTIMATE' : y_test_est}, index=test_codes_actual)
result_df.to_csv(r'D:\mysql-8.0.16-winx64\data\stock\result.csv')

plt.figure()
plt.scatter(y_test, y_test_est)
plt.xlabel('ACTUAL', fontsize=15)
plt.ylabel('ESTIMATE', fontsize=15)
plt.show()

print "Target training number of stocks = " + str(len(train_codes))
print "Actual training number of stocks = " + str(len(x_train))
print "Target testing number of stocks = " + str(len(test_codes))
print "Actual testing number of stocks = " + str(len(x_test))



