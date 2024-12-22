import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../Dataset/daily-total-female-births.csv')

dates = df['Date']
births = df['Births']

print(df.shape)
print(df.head(10))
print(df.describe())

plt.hist(births, bins=20, color='#FFBB99', edgecolor='black')
plt.xticks(rotation=90)
plt.ylabel('Date')
plt.xlabel('Births')
plt.title('Daily Total Female Births - 2')
plt.show()
