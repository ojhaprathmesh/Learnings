import numpy as np

data = np.array([12, 15, 18, 22, 26, 29, 35, 42, 50, 58])

# Calculate the IQR of a subset (e.g., first six elements)
subset_iqr = np.percentile(data[:6], 75) - np.percentile(data[:6], 25)

print(f"IQR of First Six Elements: {subset_iqr}")
