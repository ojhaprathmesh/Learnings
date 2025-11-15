import pandas as pd

data = pd.read_csv("iris-data.csv")

setosa_data = data[data['class'] == "Iris-setosa"]

mean_ratio = (setosa_data["sepal length"]/setosa_data["sepal width"]).mean()

print(f"Ratio of setosa sepal length to sepal width is {mean_ratio.round(4)}:1")

