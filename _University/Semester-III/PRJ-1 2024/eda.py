import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import missingno as msno

warnings.filterwarnings("ignore", category=UserWarning, module='openpyxl')

data = pd.read_excel('./magic_bml_data.xlsx')

print(data.head(5))

print(data.info())

print(data.describe())

print(data.isnull().sum())

plt.figure(figsize=(11, 5))
sns.countplot(x='work_start_year', data=data)
plt.title('Work Experience Start Year Distribution')
plt.show()

# Alternatively, a heatmap of missing data
plt.figure(figsize=(11, 5))
sns.heatmap(data.isnull(), cbar=False, cmap='viridis')
plt.show()

# Distribution of start and end years
plt.figure(figsize=(11, 5))
sns.histplot(data['start_year'], bins=20, kde=True)
plt.title('Distribution of Start Year')
plt.show()

# Distribution of countries
plt.figure(figsize=(11, 5))
sns.countplot(y='country', data=data, order=data['country'].value_counts().index)
plt.title('Distribution of Country')
plt.show()

# Correlation heatmap
numeric_data = data.select_dtypes(include=[float, int])

# Correlation heatmap with reduced font size
plt.figure(figsize=(10, 8))
sns.heatmap(numeric_data.corr(), annot=True, cmap='coolwarm', annot_kws={"size": 6})  # Set font size to 8
plt.title('Correlation Heatmap')
plt.show()

# Relationship between education and start year
sns.boxplot(x='highest_degree', y='start_year', data=data)
plt.title('Education Level vs Start Year')
plt.show()

# Relationship between country and job level
sns.countplot(x='job_level', hue='country', data=data)
plt.title('Job Level Distribution by Country')
plt.show()

# Boxplot to detect outliers in start and end year
plt.figure(figsize=(10, 5))
sns.boxplot(x='start_year', data=data)
plt.title('Outliers in Start Year')
plt.show()
