import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


cars_data = pd.read_csv('dataset-cars.csv')

X = cars_data[['Volume', 'Weight']]
y = cars_data['CO2']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()

model.fit(X_train, y_train)

new_data = pd.DataFrame({'Volume': [2200], 'Weight': [1500]})
predicted_co2 = model.predict(new_data)

print(f"Predicted CO2 Emission for Volume=2200, Weight=1500: {predicted_co2[0]}")
