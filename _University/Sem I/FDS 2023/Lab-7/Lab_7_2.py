import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV dataset into a DataFrame
df = pd.read_csv("../Dataset/AAPL.csv")

df['Date'] = pd.to_datetime(df['Date'])

start_date = '2022-07-01'
end_date = '2022-10-31'
filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

# Create a time series plot
plt.figure(figsize=(12.8, 8))
plt.plot(filtered_df['Date'], filtered_df['Close'], label='Stock Price')
plt.title('Stock Price Time Series (July 1, 2022, to October 31, 2022)')
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.legend()
plt.grid(True)
plt.show()
