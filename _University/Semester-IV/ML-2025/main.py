import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

url = 'https://raw.githubusercontent.com/hirdeshiitkgp/Data/refs/heads/main/Titanic.csv'
data = pd.read_csv(url)

# Display the first few rows of the data
print(data.head())

print(data.isnull().sum())

# 1. Survival rate by Class (Pclass)
survival_rate_by_class = data.groupby('Pclass')['Survived'].mean()
print("\nSurvival Rate by Class:")
print(survival_rate_by_class)

# 2. Survival rate by Gender
survival_rate_by_gender = data.groupby('Sex')['Survived'].mean()
print("\nSurvival Rate by Gender:")
print(survival_rate_by_gender)

# 3. Visualizations

# Histogram for survival distribution by class (Pclass)
plt.figure(figsize=(12, 6))
sns.histplot(data=data, x='Pclass', hue='Survived', multiple='dodge', palette='Set1', kde=False)
plt.title('Survival Distribution by Class (Pclass)')
plt.xlabel('Pclass')
plt.ylabel('Count')
plt.show()

# Histogram for survival distribution by gender (Sex)
plt.figure(figsize=(12, 6))
sns.histplot(data=data, x='Sex', hue='Survived', multiple='dodge', palette='Set2', kde=False)
plt.title('Survival Distribution by Gender')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.show()

# Filter data for survived and not survived
survived_data = data[data['Survived'] == 1]
not_survived_data = data[data['Survived'] == 0]

# Histogram for survival (Survived = 1)
plt.figure(figsize=(12, 6))
sns.histplot(survived_data, x='Age', bins=80, color='green', kde=False)
plt.title('Age Distribution for Survived Passengers')
plt.xlabel('Age')
plt.ylabel('Count')
plt.xlim(0, 80)
plt.xticks(range(0, 80, 1))
plt.show()

# Histogram for not survived (Survived = 0)
plt.figure(figsize=(12, 6))
sns.histplot(not_survived_data, x='Age', bins=80, color='red', kde=False)
plt.title('Age Distribution for Not Survived Passengers')
plt.xlabel('Age')
plt.ylabel('Count')
plt.xlim(0, 80)
plt.xticks(range(0, 80, 1))
plt.show()
