import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../Dataset/AAPL.csv')

dates = df['Date']
close = df['Close']

plt.hist(close, bins=20, color='#FFBB99', edgecolor='black')
plt.xticks(rotation=90)
plt.ylabel('Date')
plt.xlabel('Closing Price')
plt.title('Dates v/s Closing Price')
plt.show()

plt.figure(figsize=(11.2, 7))
plt.scatter(dates, close, alpha=0.2)
plt.plot(dates, close, '#FFBB99')
plt.ylabel('Date')
plt.xlabel('Closing Price')
plt.show()

for col in df.columns[1:]:
    mean_value = df[col].mean()
    print(f"Mean Value of {col}: {mean_value}")

for col in df.columns[1:]:
    std_dev = df[col].std()
    print(f"Standard Deviation of {col}: {std_dev}")
