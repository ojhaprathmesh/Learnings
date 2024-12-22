import numpy as np

data = np.array([12, 15, 18, 22, 26, 29, 35, 42, 50, 58])

# Calculate the median (50th percentile)
median = np.median(data)

# Calculate a custom quantile (e.g., 90th percentile)
quantile_90 = np.percentile(data, 90)

print(f"Median: {median}")
print(f"90th Percentile (Quantile): {quantile_90}")
