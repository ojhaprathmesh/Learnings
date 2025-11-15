import pandas as pd

data = {'Name': ['Alice', 'Bob', 'Charlie', None, 'Eve'],
        'Age': [25, 30, None, 22, 28],
        'Salary': [50000, 60000, 45000, None, 70000]}

df = pd.DataFrame(data)

# Replace missing values with the mean (for numeric columns)
df['Age'].fillna(df['Age'].mean(), inplace=True)
df['Salary'].fillna(df['Salary'].mean(), inplace=True)

print(df)
