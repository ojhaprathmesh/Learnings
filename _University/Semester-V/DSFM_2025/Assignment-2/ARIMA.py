# ARIMA Model for Time Series Forecasting for airline passengers data

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Load the dataset
url = "https://github.com/blue-yonder/pydse/blob/master/pydse/data/international-airline-passengers.csv"
data = pd.read_csv(url, parse_dates=['Month'], index_col='Month')
data = data[(data.index >= start_date) & (data.index <= end_date)]
passengers = data['Passengers']
month = data['Month']

# Plot the time series
plt.figure(figsize=(12, 6))
plt.plot(passengers, label='Monthly Passengers')
plt.title('Monthly International Airline Passengers')
plt.xlabel('Date')
plt.ylabel('Number of Passengers')
plt.legend()
plt.show()

# Fit ARIMA model
model = ARIMA(passengers, order=(5, 1, 0))  # Adjust the order as needed
model_fit = model.fit()

# Print model summary
print(model_fit.summary())

# Forecasting
forecast_steps = 12
forecast = model_fit.forecast(steps=forecast_steps)

# Plot the forecast
plt.figure(figsize=(12, 6))
plt.plot(passengers, label='Historical Data')
plt.plot(forecast, label='Forecast', color='orange')
plt.title('ARIMA Forecast')
plt.xlabel('Date')
plt.ylabel('Number of Passengers')
plt.legend()
plt.show()

# ACF and PACF plots
plt.figure(figsize=(12, 6))
plot_acf(passengers, lags=40)
plt.title('ACF of Monthly Passengers')
plt.show()
plt.figure(figsize=(12, 6))
plot_pacf(passengers, lags=40)
plt.title('PACF of Monthly Passengers')
plt.show()

