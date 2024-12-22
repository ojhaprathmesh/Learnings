import pandas as pd
data = [1, 2, None, 4, 5, 6, None, 8, 9, 10]

# Forward Fill using list comprehension
data = [val if not pd.isna(val) else data[i - 1] for i, val in enumerate(data[1:])] + [data[0]]

print("List after Forward Fill:")
print(data)
