import pandas as pd

data = pd.read_csv('IPL Ball-by-Ball 2008-2020.csv')
boundries = data[data['non_boundary'] == 0]
most_boundries = boundries.groupby('batting_team')['total_runs'].sum().idxmax()
print("Team with the highest no. of boundries:", most_boundries)

