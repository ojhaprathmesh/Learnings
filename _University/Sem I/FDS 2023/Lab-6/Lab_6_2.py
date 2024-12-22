import pandas as pd
from matplotlib import pyplot as plt

dataset = pd.read_csv('../Dataset/daily-total-female-births.csv')
births = dataset['Births']
date = dataset['Date']

x = pd.to_datetime(births)

plt.figure(figsize=(10, 8))
plt.hist(births, color='blue', edgecolor='black')
plt.ylabel('Births')
plt.xlabel('Date')
plt.title('Daily Total Female Births - 1')
plt.show()
