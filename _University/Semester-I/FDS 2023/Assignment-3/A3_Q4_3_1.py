import pandas as pd
data = [1, 2, None, 4, 5, 6, None, 8, 9, 10]

# Calculate mean excluding None values
mean_val = sum(val for val in data if pd.notna(val)) / data.count(None)

# Mean Fill using a loop
for i in range(len(data)):
    if pd.isna(data[i]):
        data[i] = mean_val

print("List after Mean Fill:")
print(data)
