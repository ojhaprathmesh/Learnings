import pandas as pd

data = pd.read_csv("StudentsPerformance.csv")

temp = data[data["gender"] == "female"]
fl_data = temp[temp["reading score"] < 70]

female_count = fl_data.shape[0]
print(f"Number of female students(reading score < 70) : {female_count}")
