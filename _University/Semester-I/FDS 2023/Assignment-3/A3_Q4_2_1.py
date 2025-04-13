import pandas as pd
data = [1, 2, None, 4, 5, 6, None, 8, 9, 10]

# Forward Fill using a loop
for i in range(len(data) - 1):
    if pd.isna(data[i]):
        data[i] = data[i - 1]

print("List after Forward Fill:")
print(data)
