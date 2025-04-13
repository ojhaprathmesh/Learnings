import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Titanic dataset
url = "https://raw.githubusercontent.com/hirdeshiitkgp/Data/refs/heads/main/Titanic.csv"
df = pd.read_csv(url)

# Basic overview
print(df.info())
print(df.isnull().sum())  # Check missing values

# Filling missing age values with median
median_age = df['Age'].median()
df.loc[:, 'Age'] = df['Age'].fillna(median_age)

# Survival rate by class and gender
plt.figure(figsize=(12, 5))
sns.barplot(x="Pclass", y="Survived", hue="Sex", data=df, palette="coolwarm")
plt.title("Survival Rate by Class and Gender")
plt.ylabel("Survival Probability")
plt.xlabel("Passenger Class")
plt.show()
""" On the doomsday of titanic, women, especially those in upper classes, were prioritized, demonstrating the women and children first protocol. This is confirmed by the plot that women in first and second class had exceptionally high survival rate, leaving very little room for uncertainty (shorter wick). 

74% of first-class passengers survived (136 out of 183).
42% of second-class passengers survived (87 out of 173).
25% of third-class passengers survived (119 out of 455).
Nearly 75% of women survived, whereas only 19% of men survived.
96% of first-class women survived, compared to 50% in second class and 49% in third class.
📊 This is reflected in the bar plot, where women, especially in upper classes, had the highest survival rates. """

# Age distribution of survivors vs non-survivors
plt.figure(figsize=(10, 5))
unique_ages = sorted(df['Age'].dropna().unique())
bins = unique_ages + [unique_ages[-1] + 1]
sns.histplot(df[df['Survived'] == 1]['Age'], bins=bins, kde=True, color='green', label='Survived')
sns.histplot(df[df['Survived'] == 0]['Age'], bins=bins, kde=True, color='red', label='Did Not Survive')
plt.title("Age Distribution of Survivors vs Non-Survivors")
plt.legend()
plt.show()
""" Devastation of titanic was also followed by inequality, your age decided your fate. Younger you were higher your rate of survival was. Those who were old cursed the women and children first protocol.
Survival rate of children (age ≤10): 59%
Survival rate of young adults (age 20-30): 38%
Survival rate of older adults (age ≥50): 22%
📊 The histogram confirms this, showing that younger passengers had a significantly higher survival probability. """

# Fare distribution across different classes
plt.figure(figsize=(12, 5))
sns.boxplot(x="Pclass", y="Fare", data=df, hue="Pclass", palette="muted", legend=False)
plt.title("Fare Distribution by Passenger Class")
plt.ylabel("Fare Amount")
plt.xlabel("Passenger Class")
plt.yscale("log")  # Log scale to handle outliers
plt.show()
""" Passengers who survived paid an average fare of $48.40, while those who didn’t survive paid an average of $13.70.
Highest fare paid: $512.33 (a first-class passenger who survived). """

# Survival rate based on fare
plt.figure(figsize=(12, 5))
sns.histplot(df[df['Survived'] == 1]['Fare'], bins=30, kde=True, color='blue', label='Survived')
sns.histplot(df[df['Survived'] == 0]['Fare'], bins=30, kde=True, color='orange', label='Did Not Survive')
plt.title("Fare Distribution Among Survivors vs Non-Survivors")
plt.legend()
plt.xscale("log")  # Log scale to show variance
plt.show()
""" This isn’t just the tale of a ship meeting an iceberg—it’s a tragedy of fate, privilege, and survival. As the Titanic sank, so did the hopes of many third-class passengers, trapped by circumstances beyond their control. While the wealthy secured lifeboats, those in steerage were left behind, their lives weighed against the price of a ticket. This wasn’t just a disaster; it was a brutal reminder that, even in the face of death, inequality reigned supreme. """

# Correlation heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(df[['Survived', 'Pclass', 'Age', 'Fare']].corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Correlation Heatmap")
plt.show()
# This heatmap visually confirms that survival is negatively correlated with class and positively correlated with fare.

print("Story Insights:")
print("1. Women and first-class passengers had higher survival rates.")
print("2. Younger passengers had a better chance of survival.")
print("3. Higher fares were associated with better survival chances.")
print("4. Class played a crucial role: third-class passengers had the lowest survival rate.")
