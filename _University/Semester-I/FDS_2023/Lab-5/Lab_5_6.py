import pandas as pd
from os import chdir

chdir("../Dataset/")

dataset = pd.read_csv("iris.csv")

print(dataset)
print(dataset.describe())
