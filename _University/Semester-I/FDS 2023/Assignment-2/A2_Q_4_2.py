import pandas as pd

data = pd.read_csv("IPL Matches 2008-2020.csv")

fl_data = data.iloc[data['toss_decision'].apply(lambda x: x == 'bat').values]

for team in fl_data["venue"].drop_duplicates():
    print(team)
    break
