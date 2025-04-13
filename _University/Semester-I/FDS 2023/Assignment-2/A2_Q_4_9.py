import pandas as pd

data = pd.read_csv('IPL Matches 2008-2020.csv', encoding='latin-1')
result_margin_counts = data["winner"].value_counts("result_margin")

highest_value_index = result_margin_counts.idxmax()

print(f'Result margin with the highest value: {highest_value_index}')

