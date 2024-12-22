import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Set the date range
start_date = '2020-05-25'
end_date = '2022-05-25'
symbol = 'AAPL'  # Apple stock symbol

# Fetch Apple stock data using yfinance
apple_stock_data = yf.download(symbol, start=start_date, end=end_date)

# Using loc functions for calculations
closing_prices = apple_stock_data['Close']

# 1. Time Series (Closing Price)
ts = closing_prices

# Plot the Time Series (Closing Price)
plt.figure(figsize=(12, 6))
plt.plot(ts.index, ts.values, label='Closing Price', color='blue')
plt.title('Apple Inc. Closing Price (May 25, 2020 - May 25, 2022)')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.show()

# 2. Mean, Median, Mode of Closing Price
mean = closing_prices.mean()
median = closing_prices.median()
mode = closing_prices.mode().iloc[0]  # In case of multiple modes, take the first one

# 3. Standard Deviation and Variance of Closing Price
std_deviation = closing_prices.std()
variance = closing_prices.var()

# Print the calculated statistics
print(f"Mean Closing Price: {mean:.2f}")
print(f"Median Closing Price: {median:.2f}")
print(f"Mode Closing Price: {mode:.2f}")
print(f"Standard Deviation of Closing Price: {std_deviation:.2f}")
print(f"Variance of Closing Price: {variance:.2f}")

# Find dates in 2020 where closing price was between 125 and maximum of 2020
closing_prices_2020 = apple_stock_data.loc['2020-01-01':'2020-12-31', 'Close']
max_price_2020 = closing_prices_2020.max()
dates_required = closing_prices_2020[
    (closing_prices_2020 >= 125) & (closing_prices_2020 <= max_price_2020)
]

print("\nDates in 2020 where closing price was between 125 and maximum of 2020:")
for date in dates_required.index:
    print(str(date).split(' ')[0])
