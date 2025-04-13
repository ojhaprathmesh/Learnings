import pandas as pd

data = pd.read_csv("StudentsPerformance.csv")

temp = data[data["gender"] == "male"]
fl_data = temp[temp["reading score"] > 70]

male_count = fl_data.shape[0]
print(f"Number of male students(reading score > 70) : {male_count}")

