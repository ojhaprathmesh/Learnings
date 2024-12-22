import pandas as pd

data = {'Name': ['Alice', 'Bob', 'Charlie', None, 'Eve'],
        'Age': [25, 30, None, 22, 28],
        'Salary': [50000, 60000, 45000, None, 70000]}

df = pd.DataFrame(data)

# Check for missing values
missing_values = df.isnull().sum()

print(f"Missing Values:\n{missing_values}")
