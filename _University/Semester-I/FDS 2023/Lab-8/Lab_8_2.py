import pandas as pd
from matplotlib import pyplot as plt
import yfinance as yf

apple_stock_data = yf.download('AAPL', start='2020-01-01', end='2023-01-01')

# Filter stock data for each year
stock_data_2020 = apple_stock_data.loc['2020-01-01':'2020-12-31']['Close']
stock_data_2021 = apple_stock_data.loc['2021-01-01':'2021-12-31']['Close']
stock_data_2022 = apple_stock_data.loc['2022-01-01':'2022-12-31']['Close']

# Create a DataFrame with the closing prices for each year
closing_prices_by_year = pd.DataFrame({
    '2020': stock_data_2020,
    '2021': stock_data_2021,
    '2022': stock_data_2022
})

# Create a bar plot to show closing prices by year
plt.figure(figsize=(10, 6))
closing_prices_by_year.mean().plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Average Apple Stock Closing Prices by Year (2020-2022)')
plt.xlabel('Year')
plt.ylabel('Average Closing Price')
plt.grid(True)
plt.xticks(rotation=0)
plt.show()
