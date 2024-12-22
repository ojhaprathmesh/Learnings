import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_excel("Alcohol_Consumption.xlsx").dropna()

# Bar plot : Weekdays
plt.figure(figsize=(10, 5))
sns.barplot(x='activities', y='Dalc', data=df)
plt.title('Average Weekday Alcohol Consumption by Extracurricular Activities')
plt.xlabel('Number of Extracurricular Activities')
plt.ylabel('Average Weekday Alcohol Consumption')
plt.show()

# Bar plot : Weekends
plt.figure(figsize=(10, 5))
sns.barplot(x='activities', y='Walc', data=df)
plt.title('Average Weekend Alcohol Consumption by Extracurricular Activities')
plt.xlabel('Number of Extracurricular Activities')
plt.ylabel('Average Weekend Alcohol Consumption')
plt.show()
