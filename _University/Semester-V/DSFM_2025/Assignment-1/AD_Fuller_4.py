# Use any publicly available stock data like Apple, Tesla, or Google and check for stationarity for price, returns and log returns.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
import yfinance as yf

data = yf.download('AAPL', start='2020-01-01', end='2023-01-01')

data['Price'] = data['Close']
data['Returns'] = data['Price'].pct_change().dropna()
data['Log Returns'] = np.log(data['Price'] / data['Price'].shift(1)).dropna()

def adf_test(series, title=''):
    result = adfuller(series.dropna())
    print(f'ADF Statistic for {title}: {result[0]}')
    print(f'p-value: {result[1]}')
    print('Critical Values:')
    for key, value in result[4].items():
        print(f'  {key}: {value}')
    if result[1] < 0.05:
        print(f'The {title} series is likely stationary.')
    else:
        print(f'The {title} series is likely non-stationary.')

adf_test(data['Price'], 'Price')
adf_test(data['Returns'], 'Returns')
adf_test(data['Log Returns'], 'Log Returns')

plt.figure(figsize=(15, 10))
plt.subplot(3, 1, 1)
plt.plot(data['Price'], label='Price')
plt.title('Stock Price')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(data['Returns'], label='Returns', color='orange')
plt.title('Returns')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(data['Log Returns'], label='Log Returns', color='green')
plt.title('Log Returns')
plt.legend()

plt.tight_layout()
plt.show()