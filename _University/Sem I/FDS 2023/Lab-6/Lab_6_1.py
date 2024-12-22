import pandas as pd
from matplotlib import pyplot as plt

dataset = pd.read_csv('../Dataset/daily-total-female-births.csv')
y = dataset['Births']
x = dataset['Date']

x = pd.to_datetime(x)

plt.figure(figsize=(14.4, 9))
plt.scatter(x, y, alpha=0.2)
plt.plot(x, y, '#FFBB99')
plt.ylabel('Births')
plt.xlabel('Date')
plt.title('Daily Total Female Births - 1')
plt.show()
