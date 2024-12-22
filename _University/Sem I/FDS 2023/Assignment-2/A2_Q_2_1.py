import pandas as pd

data = pd.read_csv("iris-data.csv")
parameters = ['sepal length', 'sepal width', 'petal length', 'petal width']

for param in parameters:
    print(f"Mean of {param} : {data[param].mean()}")

for param in parameters:
    print(f"Median of {param} : {data[param].median()}")

for param in parameters:
    print(f"Standard Deviation of {param} : {data[param].std()}")

