import pandas as pd

data = pd.read_csv("StudentsPerformance.csv")

male_data = data[data["gender"] == "male"]
score_data = male_data[male_data["reading score"] >= 80]
score_data = score_data[score_data["reading score"] <= 90]

print(score_data.describe())  # This lets me know that i have selected required data

print(f"Number of male students: {score_data.shape[0]}")
