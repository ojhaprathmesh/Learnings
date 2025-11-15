import pandas as pd

data = pd.read_csv("iris-data.csv")

features = {
    "sepal length": 0,
    "sepal width": 0,
    "petal length": 0,
    "petal width": 0
}

max_var = [0, '']
for feature in features.keys():
    features[feature] = data[feature].var()
    if max_var[0] < features[feature]:
        max_var = [features[feature], feature]

print(f"{max_var[1].capitalize()} is the best feature "
      f"due to its high variance of {max_var[0]}")

