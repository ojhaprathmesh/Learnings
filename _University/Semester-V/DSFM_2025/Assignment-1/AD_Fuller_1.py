import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

np.random.seed(0)
n = 100
a = np.zeros(n)
epsilon = np.random.normal(0, 1, n)

for t in range(1, n):
    a[t] = 0.7 * a[t-1] + epsilon[t]

# Augmented Dickey-Fuller test
result = adfuller(a)
print("ADF Statistic:", result[0])
print("p-value:", result[1])
print("Critical Values:", result[4])
if result[1] < 0.05:
    print("The time series is likely stationary.")
else:
    print("The time series is likely non-stationary.")

plt.plot(a)
plt.title("AR(1) Time Series: a(t) = 0.7a(t-1) + e(t)")
plt.xlabel("Time (t)")
plt.ylabel("a(t)")
plt.show()

