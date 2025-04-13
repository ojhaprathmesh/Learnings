import numpy as np

data = np.array([12, 15, 18, 22, 26, 29, 35, 42, 50, 58])

# Calculate the 10-90 quantile range
quantile_10 = np.percentile(data, 10)
quantile_90 = np.percentile(data, 90)
quantile_range = quantile_90 - quantile_10

print(f"10th Quantile: {quantile_10}")
print(f"90th Quantile: {quantile_90}")
print(f"Quantile Range: {quantile_range}")
