import pandas as pd

data = pd.read_csv("iris-data.csv")

species = {
    "Iris-setosa": 0,
    "Iris-versicolor": 0,
    "Iris-virginica": 0
}

for sample in data["class"]:
    species[sample] += 1

for name, num in species.items():
    print(f"There are {num} samples of {name}")

