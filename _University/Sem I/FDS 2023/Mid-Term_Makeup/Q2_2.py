import pandas as pd

data = pd.read_csv("StudentsPerformance.csv")
male_data = data[data["gender"] == "male"]
rq_data = male_data[male_data["race/ethnicity"] == "group A"]

print(f"Number of Males: {rq_data.shape[0]}")

