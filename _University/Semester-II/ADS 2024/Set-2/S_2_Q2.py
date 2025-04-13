import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_excel("Alcohol_Consumption.xlsx").dropna()

# Box plot : Weekdays
plt.figure(figsize=(10, 5))
sns.boxplot(x='famrel', y='Dalc', data=df)
plt.title('Weekday Alcohol Consumption by Family Relationship Quality')
plt.xlabel('Quality of Family Relationships')
plt.ylabel('Weekday Alcohol Consumption')
plt.show()

# Box plot : Weekends
plt.figure(figsize=(10, 5))
sns.boxplot(x='famrel', y='Walc', data=df)
plt.title('Weekend Alcohol Consumption by Family Relationship Quality')
plt.xlabel('Quality of Family Relationships')
plt.ylabel('Weekend Alcohol Consumption')
plt.show()
