import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
data = pd.read_csv("Power_Grid_Data.csv").dropna().drop_duplicates()

# Define the column of interest
column_of_interest = 'SLPR7:Voltage A:Magnitude'

# Calculate the interquartile range (IQR) for the column of interest
Q1 = data[column_of_interest].quantile(0.25)
Q3 = data[column_of_interest].quantile(0.75)
IQR = Q3 - Q1

# Define the desired sample size
sample_size = 3000  # Adjust this value based on the size of your dataset and desired plot resolution

# Generate random samples within the IQR range
random_sample = data[(data[column_of_interest] >= Q1) & (data[column_of_interest] <= Q3)].sample(sample_size)

# Create a subplot with 2 rows and 1 column
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Plot SLPR7:Voltage A:Magnitude vs Timestamp with random sampling
ax1.plot(random_sample['Timestamp'], random_sample['SLPR7:Voltage A:Magnitude'], '.')
ax1.set_title('SLPR7:Voltage A:Magnitude vs Timestamp (Random Sample within IQR)')
ax1.set_xlabel('Timestamp')
ax1.set_ylabel('Voltage A:Magnitude')
ax1.tick_params(axis='x', rotation=90)  # Rotate x-axis labels by 90 degrees

# Plot SLPR7:Voltage A:Magnitude vs Frequency with random sampling
ax2.plot(random_sample['SLPR7:Voltage A:Magnitude'], random_sample['SLPR7:Frequency'], '.')
ax2.set_title('SLPR7:Voltage A:Magnitude vs Frequency (Random Sample within IQR)')
ax2.set_xlabel('Voltage A:Magnitude')
ax2.set_ylabel('Frequency')

plt.tight_layout()  # Adjust subplot layout to prevent overlapping
plt.show()
