import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("CardioGoodFitness.csv")

# Histogram with a smooth line plot
sns.set(style="white")
sns.histplot(data=df, x='Age', kde=True, color='blue', edgecolor='black')
plt.title('Distribution of Age')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# Line Plot
age_counts = df['Age'].value_counts().sort_index()

plt.plot(age_counts, marker='o', color='black')
plt.title('Count of Each Age')
plt.xlabel('Age')
plt.ylabel('Count')
plt.tight_layout()
plt.show()

# Pie chart
labels = ['Male', 'Female']
male_count = len(df[df['Gender'] == 'Male'])
female_count = len(df[df['Gender'] == 'Female'])
values = [male_count, female_count]

plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=0, colors=['skyblue', 'lightpink'])
plt.title("Gender Distribution")
plt.show()

# Bar plot
grouped = df.groupby(['MaritalStatus', 'Gender']).size().unstack()
grouped = grouped.iloc[::-1]
print(grouped)
grouped.plot(kind='bar', color=['blue', 'orange'], alpha=0.75)
plt.xlabel('Marital Status')
plt.ylabel('Count')
plt.title('Gender vs. Marital Status')
plt.xticks(rotation=0)
plt.legend(title='Gender', title_fontsize='large', loc='upper left', labels=['Male', 'Female'], facecolor='white')
plt.show()

# Box Plot - Male vs Female
sns.boxplot(data=df, x='Gender', y='Age', palette={'Male': 'blue', 'Female': 'orange'})
plt.title('Distribution of Age by Gender')
plt.xlabel('Gender')
plt.ylabel('Age')
plt.tight_layout()
plt.show()

sns.set(style="white")

# Box Plot for Product vs Age
sns.boxplot(data=df, x='Product', y='Age', palette='Set2')
plt.title('Product vs Age')
plt.xlabel('Product')
plt.ylabel('Age')
plt.tight_layout()
plt.show()

# Box Plot for Age vs Fitness
sns.boxplot(data=df, x='Age', y='FitnessScore', palette='Set3')
plt.title('Age vs Fitness')
plt.xlabel('Age')
plt.ylabel('Fitness')
plt.tight_layout()
plt.show()

# Box Plot for Gender vs Fitness
sns.boxplot(data=df, x='Gender', y='FitnessScore', palette={'Male': 'blue', 'Female': 'orange'})
plt.title('Gender vs Fitness')
plt.xlabel('Gender')
plt.ylabel('Fitness')
plt.tight_layout()
plt.show()

df_encoded = pd.get_dummies(df, columns=['Product', 'Gender', 'MaritalStatus'])

# Calculate the correlation matrix
correlation_matrix = df_encoded.corr()

# Plot the correlation matrix using Seaborn
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Correlation Plot of Cardio Fitness Data')
plt.tight_layout()
plt.show()
