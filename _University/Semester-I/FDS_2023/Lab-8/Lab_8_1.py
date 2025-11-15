from matplotlib import pyplot as plt
import yfinance as yf

apple_stock_data = yf.download('AAPL', start='2020-01-01', end='2023-01-01')

# Extract the year from the Date column and filter stock data for each year
apple_stock_data['Year'] = apple_stock_data.index.year

stock_data_2020 = apple_stock_data[apple_stock_data['Year'] == 2020]['Close']
stock_data_2021 = apple_stock_data[apple_stock_data['Year'] == 2021]['Close']
stock_data_2022 = apple_stock_data[apple_stock_data['Year'] == 2022]['Close']

# Plot separate histograms for each year with different colors
plt.figure(figsize=(15, 6))

plt.subplot(1, 3, 1)
plt.hist(stock_data_2020, bins=30, color='orange', edgecolor='black')
plt.title('Histogram of Apple Stock Closing Prices (2020)')
plt.xlabel('Closing Price')
plt.ylabel('Frequency')
plt.grid(True)

plt.subplot(1, 3, 2)
plt.hist(stock_data_2021, bins=30, color='white', edgecolor='black')  # Changed color to orange
plt.title('Histogram of Apple Stock Closing Prices (2021)')
plt.xlabel('Closing Price')
plt.ylabel('Frequency')
plt.grid(True)

plt.subplot(1, 3, 3)
plt.hist(stock_data_2022, bins=30, color='green', edgecolor='black')  # Changed color to green
plt.title('Histogram of Apple Stock Closing Prices (2022)')
plt.xlabel('Closing Price')
plt.ylabel('Frequency')
plt.grid(True)

plt.tight_layout()
plt.show()

# Credits @nick_kerr6