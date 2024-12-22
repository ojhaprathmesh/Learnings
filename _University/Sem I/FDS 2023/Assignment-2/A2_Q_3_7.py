import pandas as pd

data = pd.read_csv("StudentsPerformance.csv")

male_count = data[data["gender"] == "male"].shape[0]
female_count = data[data["gender"] == "female"].shape[0]

sex_ratio = female_count/male_count

print(f"There are {round(sex_ratio*1000)} females per 1000 males")
