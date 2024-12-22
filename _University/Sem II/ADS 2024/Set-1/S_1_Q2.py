import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_excel('Alcohol_Consumption.xlsx')

grouped_data = df.groupby(['sex', 'health']).agg({
    'Dalc': 'mean',
    'Walc': 'mean'
}).reset_index()

plt.figure(figsize=(12, 6))

# Bar plot for alcohol consumption during workdays
plt.subplot(1, 2, 1)
sns.barplot(x='health', y='Dalc', hue='sex', data=grouped_data)
plt.title('Average Alcohol Consumption During Workdays by Health Status')

# Bar plot for alcohol consumption during weekends
plt.subplot(1, 2, 2)
sns.barplot(x='health', y='Walc', hue='sex', data=grouped_data)
plt.title('Average Alcohol Consumption During Weekends by Health Status')

plt.tight_layout()
plt.show()