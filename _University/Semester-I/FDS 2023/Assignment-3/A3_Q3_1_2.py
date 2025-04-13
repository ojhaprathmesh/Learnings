import numpy as np

data = np.array([12, 15, 18, 22, 26, 29, 35, 42, 50, 58])

# Calculate the interquartile range (IQR)
iqr = np.percentile(data, 75) - np.percentile(data, 25)

print(f"Interquartile Range (IQR): {iqr}")
