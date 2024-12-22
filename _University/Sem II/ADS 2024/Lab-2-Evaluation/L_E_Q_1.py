import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Loading data
df = pd.read_csv('Car_Details.csv')

# Splitting data into features (X) and target variable (y)
y = df["selling_price"]
y_mean = y.mean()
print(y_mean)

n = len(df)

x = df["km_driven"]
x_mean = x.mean()

Y_n = sum(x * y) - n * x_mean * y_mean
X_n = sum(x * x) - n * x_mean * x_mean

x1 = Y_n / X_n

x0 = y_mean - x1 * x_mean
print(f"Slope is {x1}")
print(f"Intercept is {x0}")

y_pred = x1 * x + x0

print(f"The equation of regression is {y_pred}")

plt.scatter(x, y, color='orange')
plt.plot(x, y_pred, color='cyan')
plt.show()
#
# import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split
#
# # Load the dataset
# df = pd.read_csv("Car_Details.csv")
#
# # Select features and target variable
# X = df[['year', 'km_driven']]
# y = df['selling_price']
#
# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#
# # Create and fit the linear regression model
# model = LinearRegression()
# model.fit(X_train, y_train)
#
# # Predict the selling price
# y_pred = model.predict(X_test)
#
# # Calculate the regression line equation
# slope = model.coef_
# intercept = model.intercept_
# print("Regression Line Equation: y =", slope[0], "* year +", slope[1], "* km_driven +", intercept)
#
# # Plot the regression line
# plt.scatter(X_test['year'], y_test, color='blue', label='Actual Selling Price')
# plt.plot(X_test['year'], y_pred, color='red', label='Predicted Selling Price')
# plt.xlabel('Year')
# plt.ylabel('Selling Price')
# plt.title('Regression Line')
# plt.legend()
# plt.show()
