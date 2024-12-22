import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("Footballdata.csv").drop_duplicates().dropna()

# Bar plot
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
sns.countplot(data=df, x='Preferred Foot', hue='Preferred Foot', orient='v')
plt.title("Distribution of Players by Preferred Foot")
plt.xlabel("Preferred Foot")
plt.ylabel("Count of Players")
plt.grid(axis='y', linestyle='--', alpha=0.75)

# Pie chart
labels = ['Left', 'Right']
left_count = len(df[df['Preferred Foot'] == 'Left'])
right_count = len(df[df['Preferred Foot'] == 'Right'])
values = [left_count, right_count]

plt.subplot(1, 2, 2)
plt.pie(values, labels=labels, autopct="%1.2f%%", startangle=0, colors=['cyan', 'orange'],
        wedgeprops=dict(edgecolor='black'))
plt.title("Foot Preference Distribution")
plt.show()

# Vertical bar plot
req = df.groupby('Nationality').size()
req = req.sort_values(ascending=False).iloc[:10]

plt.figure(figsize=(12, 5))
sns.countplot(data=df[df['Nationality'].isin(req.index)],
              x='Nationality', order=req.index)
plt.xlabel('Nationality')
plt.ylabel('Count')
plt.title('Top 10 Nationalities')
plt.grid(axis='y', linestyle='--', alpha=0.75)
plt.show()
