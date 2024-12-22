import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("IRIS.csv").dropna()
df.drop_duplicates(inplace=True)

# Bar plot
min_value = int(df['sepal_length'].min())
max_value = round(df['sepal_length'].max())
bins = []

for i in range(min_value, max_value + 1):
    bins.append(i)

df['sepal_length_bin'] = pd.cut(df['sepal_length'], bins=bins)

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
sns.countplot(data=df, x='sepal_length_bin', hue='sepal_length_bin')
plt.title("Distribution of Sepal Length")
plt.xlabel("Sepal Length Range")
plt.ylabel("Count of Observations")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.75)
plt.legend(title="Range")

# Histogram
plt.subplot(1, 2, 2)
sns.histplot(data=df, x='sepal_width', kde=False, color='skyblue', bins=20)
plt.title("Distribution of Sepal Width")
plt.xlabel("Sepal Width")
plt.ylabel("Frequency")
plt.grid(axis='y', linestyle='--', alpha=0.75)
plt.show()
