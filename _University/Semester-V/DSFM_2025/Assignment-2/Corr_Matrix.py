# SP500 Correlation Matrix for last 10 years

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Define the start and end dates for the last 10 years
end_date = datetime.now()
start_date = end_date - timedelta(days=3650)  # 10 years

# List of S&P 500 companies (tickers)
sp500_tickers = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'BRK-B', 'NVDA', 'JPM', 'V',
]

# Download historical data for the S&P 500 companies
# Use auto_adjust=False to get separate 'Adj Close' column, or use 'Close' with auto_adjust=True
raw_data = yf.download(sp500_tickers, start=start_date, end=end_date, auto_adjust=False, progress=False)

# Extract 'Adj Close' data - handle MultiIndex structure
if len(sp500_tickers) > 1:
    # Check if 'Adj Close' exists, otherwise use 'Close'
    if 'Adj Close' in raw_data.columns.get_level_values(0):
        data = raw_data['Adj Close']
    else:
        data = raw_data['Close']
else:
    # For single ticker, yfinance returns different structure
    if 'Adj Close' in raw_data.columns.get_level_values(0):
        data = raw_data['Adj Close'].to_frame(sp500_tickers[0])
    else:
        data = raw_data['Close'].to_frame(sp500_tickers[0])

# Drop rows with any NaN values
data.dropna(inplace=True)

# Calculate the daily returns
returns = data.pct_change().dropna()

# Calculate the correlation matrix
correlation_matrix = returns.corr()

# Plot the correlation matrix
plt.figure(figsize=(12, 8))
plt.imshow(correlation_matrix, cmap='coolwarm', interpolation='none')
plt.colorbar()
plt.xticks(range(len(correlation_matrix.columns)), correlation_matrix.columns, rotation=90)
plt.yticks(range(len(correlation_matrix.index)), correlation_matrix.index)
plt.title('S&P 500 Correlation Matrix (Last 10 Years)')
plt.tight_layout()
plt.show()

# Save the correlation matrix to a CSV file
correlation_matrix.to_csv('sp500_correlation_matrix.csv')

# Print the correlation matrix
print(correlation_matrix)

# Save the correlation matrix to a file
correlation_matrix.to_csv('sp500_correlation_matrix.csv')

# Print the correlation matrix
print("Correlation Matrix:")
print(correlation_matrix)