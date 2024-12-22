import pandas as pd
from scipy.stats import zscore

# Read your dataset into a DataFrame
df = pd.read_excel("outlier_example2.xlsx")

# IQR Method
Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers_iqr = (df < lower_bound) | (df > upper_bound)

# z score Method

z_scores = df.apply(zscore)

z_threshold = 1.7

outliers_zscore = (z_scores > z_threshold) | (z_scores < -z_threshold)

print("Outliers detected using IQR method:")
print(outliers_iqr)
print()
print("Outliers detected using Z-score method:")
print(outliers_zscore)
