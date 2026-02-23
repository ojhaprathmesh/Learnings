# Write a code to generate these four equations: y(1) = mt + c, y(2) = 10 sin(2pi t / 10), y(3) = 50 sin(2pi t / 60), y(4) = epsilon(t). Then add them together to create a time series y(t) = y(1) + y(2) + y(3) + y(4). Finally, perform the Augmented Dickey-Fuller test on the resulting time series. Also find the range of the values of m such that the time series is stationary using a loop. The precision of the answer should be upto three decimal places. Use the random seed 42 for white noise generation.

import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

np.random.seed(42)
n = 100
t = np.arange(n)
m_values = np.arange(-10, 11, 0.001)  # Slopes from -10 to 10 with step 0.001
epsilon = np.random.normal(0, 1, n)
stationary_m = []

for m in m_values:
    y1 = m * t + 5  # y(1) = mt + c, where c = 5
    y2 = 10 * np.sin(2 * np.pi * t / 10)
    y3 = 50 * np.sin(2 * np.pi * t / 60)
    y4 = epsilon
    y = y1 + y2 + y3 + y4

    # Perform Augmented Dickey-Fuller test
    result = adfuller(y)
    if result[1] < 0.05:  # If p-value is less than 0.05, series is stationary
        stationary_m.append(m)

# Print the range of m values for which the series is stationary
print(f"Range of m values for stationarity: {stationary_m[0]:.3f} to {stationary_m[-1]:.3f}")

# Plot the time series
plt.figure(figsize=(12, 6))
plt.plot(t, y, label='y(t) = y(1) + y(2) + y(3) + y(4)')
plt.title('Time Series y(t)')
plt.xlabel('Time (t)')
plt.ylabel('y(t)')
plt.legend()
plt.show()
