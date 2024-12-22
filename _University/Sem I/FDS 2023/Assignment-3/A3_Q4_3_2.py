import pandas as pd
data = [1, 2, None, 4, 5, 6, None, 8, 9, 10]

# Calculate mean excluding None values
mean_val = sum(val for val in data if pd.notna(val)) / data.count(None)

# Mean Fill using list comprehension
data = [val if not pd.isna(val) else mean_val for val in data]

print("List after Mean Fill:")
print(data)
