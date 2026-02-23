import numpy as np
from scipy.stats import skew, kurtosis
import yfinance as yf
import matplotlib.pyplot as plt

def analyze_stock(stock, start_date, end_date):
    data = yf.download(stock, start=start_date, end=end_date)
    
    if data.empty:
        print(f"No data found for {stock}.")
        return None

    # Calculate log returns
    data['Log Returns'] = np.log(data['Close'] / data['Close'].shift(1))
    log_returns = data['Log Returns'].dropna()

    # Calculate skewness and kurtosis
    skewness = skew(log_returns)
    kurt = kurtosis(log_returns)  # excess kurtosis

    # Print results
    print(f"{stock} - Skewness: {skewness:.4f}, Kurtosis: {kurt:.4f}")

    # Plot log returns
    plt.figure(figsize=(10, 5))
    plt.plot(log_returns)
    plt.axhline(0, color='red', linestyle='--')
    plt.title(f'Log Returns of {stock}')
    plt.xlabel('Date')
    plt.ylabel('Log Return')
    plt.grid(True)
    plt.show()

    return {'Skewness': skewness, 'Kurtosis': kurt, 'Log Returns': log_returns}

start_date = '2015-01-01'
end_date = '2025-01-01'
results = {}

results['AAPL'] = analyze_stock('AAPL', start_date, end_date)
results['GOOGL'] = analyze_stock('GOOGL', start_date, end_date)
results['MSFT'] = analyze_stock('MSFT', start_date, end_date)

# Using Q-Q plot to visualize normality
import scipy.stats as stats

def qq_plot(data, stock):
    stats.probplot(data['Log Returns'].dropna(), dist="norm", plot=plt)
    plt.title(f'Q-Q Plot for {stock}')
    plt.xlabel('Theoretical Quantiles')
    plt.ylabel('Sample Quantiles')
    plt.grid(True)
    plt.show()

for stock in results.keys():
    data = yf.download(stock, start=start_date, end=end_date)
    qq_plot(data, stock)
