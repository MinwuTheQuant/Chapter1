# PART 1: draw in stock price data

# 1. pandas_datareader is a library for stock price data
from pandas_datareader import data
# 2. Set the start_date as 2020-01-01
start_date = '2020-01-01'
# 3. Set the ending data as 2022-03-01
end_date = '2022-03-01'
# 4. Load the data of TSLA from yahoo using DataReader library (attributes: ticker, yahoo, start_date, end_date)
tsla_data = data.DataReader('GOOG', 'yahoo', start_date, end_date)

# import numpy and pandas for matrix usage
import numpy as np
import pandas as pd

# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 1000)
# print(tsla_data)

###############################################################################

# Part 2: Signal Generation
# Strategy: Buy low sell high: comparison of close price of two consecutive days. buy if negative, sell if positive

# 1. Copy data with the same dimension, named tsla_data_signal (index can be understood as a concept of row)
tsla_data_signal=pd.DataFrame(index=tsla_data.index)
# 2. Signal price: adj close of original dataframe tsla_data
tsla_data_signal['price']=tsla_data['Adj Close']
# 3. diff(): utilize the diff: difference of each row in the column
tsla_data_signal['daily difference']=tsla_data_signal['price'].diff()
# 4. Buy and sell signal (1 if positive, 0 if negative)
tsla_data_signal['signal']=0.0
tsla_data_signal['signal']=np.where(tsla_data_signal['daily difference'][:]> 0,1.0,0.0)
# 5. Say no multiple buy and sell is available. Therefore we give a constraint by diff
tsla_data_signal['positions']=tsla_data_signal['signal'].diff()
# print(tsla_data_signal)

###############################################################################
# Part 3. Signal visualization
# 1. Import library
import matplotlib.pyplot as plt
# 2. Draw the graph
fig=plt.figure()
ax1=fig.add_subplot(111,ylabel='Tesla price in $')
tsla_data_signal['price'].plot(ax=ax1,color='r',lw=2)

# 3. buy sign, sell sign (buy when position is 1)
ax1.plot(tsla_data_signal.loc[tsla_data_signal.positions == 1.0].index,
         tsla_data_signal.price[tsla_data_signal.positions == 1.0],
         '^', markersize=3, color='m')
# 4. Likewise, sell sign
ax1.plot(tsla_data_signal.loc[tsla_data_signal.positions == -1.0].index,
         tsla_data_signal.price[tsla_data_signal.positions == -1.0],
         'v', markersize=3, color='k')
#plt.show()

###############################################################################

# PART 4. Backtesting
# 1. Start with 1000 USD
initial_capital=float(10000.0)
# 2. Dataframe for positions and portfolio
positions=pd.DataFrame(index=tsla_data_signal.index).fillna(0.0)
portfolio=pd.DataFrame(index=tsla_data_signal.index).fillna(0.0)
# 3. Save signals of 'TSLA' into positions dataframe
positions['TSLA']=tsla_data_signal['signal']
# 4. Save magnitude of position (price*position)
portfolio['positions']=(positions.multiply(tsla_data_signal['price'],axis=0))
# 5. Calculate cash
portfolio['cash'] = initial_capital-(positions.diff().multiply(tsla_data_signal['price'], axis=0)).cumsum()
# 6. total is the sum
portfolio['total'] = portfolio['positions'] + portfolio['cash']
print(portfolio)
# 7. plot it
portfolio.plot()
plt.show()

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='Portfolio value in $')
portfolio['total'].plot(ax=ax1, lw=2.)
#ax1.plot(portfolio.loc[tsla_data_signal.positions == 1.0].index,portfolio.total[tsla_data_signal.positions == 1.0],'^', markersize=10, color='m')
#ax1.plot(portfolio.loc[tsla_data_signal.positions == -1.0].index,portfolio.total[tsla_data_signal.positions == -1.0],'v', markersize=10, color='k')
#plt.show()