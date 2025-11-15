import pandas as pd
data = [1, 2, None, 4, 5, 6, None, 8, 9, 10]

# Backward Fill using list comprehension
data = [data[i + 1] if pd.isna(val) else val for i, val in enumerate(data[:-1])] + [data[-1]]

print("List after Backward Fill:")
print(data)
