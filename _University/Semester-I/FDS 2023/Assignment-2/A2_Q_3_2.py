import pandas as pd

data = pd.read_csv("StudentsPerformance.csv")

groups = {'group A': 0, 'group B': 0, 'group C': 0, 'group D': 0, 'group E': 0}

for member in data["race/ethnicity"]:
    groups[member] += 1

for name, count in groups.items():
    print(f"{name.capitalize()} has {count} male students")

