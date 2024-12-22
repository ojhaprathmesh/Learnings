import numpy as np

data = np.array([12, 15, 18, 22, 26, 29, 35, 42, 50, 100])

# Identify outliers using the IQR method
q1 = np.percentile(data, 25)
q3 = np.percentile(data, 75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
outliers = [x for x in data if x < lower_bound or x > upper_bound]

print(f"Outliers: {outliers}")
