# Write a code to use the given github data link to perform decomposition on the time series data and plot the components.

import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# Load the dataset
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv"
data = pd.read_csv(url, header=0, parse_dates=[0], index_col=0)

# Perform seasonal decomposition
result = seasonal_decompose(data, model='additive')

result.plot()
plt.show()