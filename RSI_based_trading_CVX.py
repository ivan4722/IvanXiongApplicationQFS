import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from datetime import timezone
import pandas as pd
import numpy as np
import pytz

'''

Algorithm to calculate RSI at every data point
Picks RSI points, user may specify a day range to sell after the selected date based on the calculated RSI 

@author Ivan Xiong

'''

start_date = '2021-10-21'
end_date = '2023-09-21'
stock_data = {}

# Fetch data at hourly intervals
stock = 'CVX'
data = yf.download(stock, start=start_date, end=end_date, interval='1h')
stock_data = data


def calculate_rsi(data, window=14):
    close_prices = data['Close']
    delta = close_prices.diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


data['RSI'] = calculate_rsi(data)

#plotting RSI (uncomment to use)

plt.figure(figsize=(12, 6))
plt.plot(data['RSI'], label='RSI')
plt.title(stock+' RSI')
plt.xlabel('Date')
plt.ylabel('RSI')
plt.legend()
plt.grid()
plt.show()


cvx_less_than_threshold = []
#dt defined so I don't sell the stock in the future, where there is obviously no data
dt = datetime(year=2023, month=8, day=21, hour=12, minute=0, second=0)
est = pytz.timezone('US/Eastern')
dt_est = est.localize(dt)

bestrsi=0
bestprofit=-9999
profit=-999
#numtrades=0
for i in range(1,31,1):
    rsi_threshold=i
    for date, rsi_value in stock_data['RSI'].items():
        if rsi_value <= rsi_threshold and date < dt_est:
            cvx_less_than_threshold.append(date)

    sumbuy = 0
    sumsell = 0


    for a in cvx_less_than_threshold:
        date_30_days_later = a + timedelta(days=28)
        if a in stock_data.index and date_30_days_later in stock_data.index:
            sumbuy += stock_data['Close'][a]
            sumsell += stock_data['Close'][date_30_days_later]
            
    
    if sumsell!=0:
        profit = (sumsell-sumbuy)/sumbuy *100
    if profit > bestprofit:
        bestprofit=profit
        bestrsi=rsi_threshold
    print('rsi:', rsi_threshold)
    print('Total amount spent on buying:', sumbuy)
    print('Total amount received from selling:', sumsell)
    print("percent profit: ", profit)
print("best rsi:", bestrsi, "with profit of: ", bestprofit)
#print("numtrades: ", numtrades)