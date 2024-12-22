import pandas as pd

data = pd.read_csv("StudentsPerformance.csv")

temp = data[data["lunch"] == "standard"]
fl_data = temp[temp["gender"] == "female"]

count = fl_data.shape[0]
print(f"Number of female students having standard lunch : {count}")

