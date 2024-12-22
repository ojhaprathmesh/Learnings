import pandas as pd
import matplotlib.pyplot as plt

# Read the data and drop NaN values
df = pd.read_excel("Alcohol_Consumption.xlsx").dropna()

# Calculate the correlation
correlation_matrix = df[['Medu', 'Fedu']].corr()

# Extract the correlation coefficient between 'Medu' and 'Fedu'
correlation_coefficient = correlation_matrix.iloc[0, 1]

# Plot the correlation coefficient using a bar chart
plt.figure(figsize=(8, 6))
plt.bar(['Medu vs Fedu'], [correlation_coefficient], color='skyblue')
plt.title("Correlation between Parents' Education Levels")
plt.xlabel('Features')
plt.ylabel('Correlation Coefficient')
plt.ylim(-1, 1)  # Set the y-axis limit to match the range of correlation coefficients (-1 to 1)
plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)  # Add a horizontal line at y=0 for reference
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add grid lines for better visualization
plt.show()
