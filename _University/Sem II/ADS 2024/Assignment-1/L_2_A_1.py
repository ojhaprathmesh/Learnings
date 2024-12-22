import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv")

print(df.dtypes)

df.drop(columns=['Popularity', 'Number of Doors', 'Vehicle Size'], inplace=True)

print(df.shape)

df.drop_duplicates(inplace=True)

print(df.shape)

df.dropna(inplace=True)

print(df)


def detect_outliers(column):
    Q1 = np.percentile(column, 25)
    Q3 = np.percentile(column, 75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = column[(column < lower) | (column > upper)]
    return outliers


print(f"Outliers in MSRP: {detect_outliers(df['MSRP'])}\n")

print(f"Outliers in Cylinders: {detect_outliers(df['Engine Cylinders'])}\n")

print(f"Outliers in Horsepower:{detect_outliers(df['Engine HP'])}")

plt.figure(figsize=(13, 6))

plt.subplot(1, 2, 1)  # 1 row, 2 columns, subplot 1
plt.scatter(df['Engine HP'], df['MSRP'])
plt.xlabel('Horsepower')
plt.ylabel('Price')
plt.title('Scatter Plot')

# Count the number of cars for each make
car_counts = df['Make'].value_counts()

# Plot the histogram
plt.subplot(1, 2, 2)  # 1 row, 2 columns, subplot 2
car_counts.plot(kind='bar', color='skyblue')
plt.title('Number of Cars by Make')
plt.xlabel('Make')
plt.ylabel('Number of Cars')
plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
plt.tight_layout()

plt.show()
