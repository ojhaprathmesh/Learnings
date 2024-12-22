import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("IRIS.csv").drop_duplicates().dropna()

# Scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='sepal_width', y='petal_length', hue='species', palette='Set1')
plt.title("Scatter Plot of Sepal Width vs. Petal Length")
plt.xlabel("Sepal Width")
plt.ylabel("Petal Length")
plt.legend(title='Species')
plt.grid(True)
plt.show()

# Pairwise plot
sns.pairplot(df, hue='species', palette='Set1', markers=['o', 's', 'D'])
plt.suptitle("Pairwise Plot of Iris Dataset", y=1.02)
plt.show()
