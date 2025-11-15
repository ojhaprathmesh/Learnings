import numpy as np

data = np.array([12, 15, 18, 22, 26, 29, 35, 42, 50, 58])

# Calculate the first quartile (Q1)
q1 = np.percentile(data, 25)

# Calculate the third quartile (Q3)
q3 = np.percentile(data, 75)

print(f"First Quartile (Q1): {q1}")
print(f"Third Quartile (Q3): {q3}")
