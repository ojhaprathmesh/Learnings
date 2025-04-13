import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_excel('Alcohol_Consumption.xlsx')

grouped_data = df.groupby('health').agg({
    'Dalc': 'mean'
}).reset_index()

plt.figure(figsize=(12, 6))

# Bar plot for alcohol consumption during workdays
sns.barplot(x='health', y='Dalc', data=grouped_data)
plt.title('Average Alcohol Consumption During Workdays by Health Status')
plt.show()

grouped_data = df.groupby('traveltime').agg({
    'failures': 'mean'
}).reset_index()


plt.figure(figsize=(12, 6))

# Bar plot for alcohol consumption during workdays
sns.barplot(x='traveltime', y='failures', data=grouped_data)
plt.title('Travelling time vs Failure')
plt.show()
