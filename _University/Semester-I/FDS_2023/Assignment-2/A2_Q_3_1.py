import pandas as pd

data = pd.read_csv("StudentsPerformance.csv")

fl_data = data[data["gender"] == "female"]

female_count = fl_data.shape[0]
print(f"Number of female students : {female_count}")

