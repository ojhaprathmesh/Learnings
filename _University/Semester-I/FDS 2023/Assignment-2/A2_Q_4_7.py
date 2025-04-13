import pandas as pd

data = pd.read_csv('IPL Matches 2008-2020.csv', encoding='latin-1')
toss_impact = (data[data['toss_winner'] == data['winner']]['team1'].value_counts() +
               data[data['toss_winner'] == data['winner']]['team2'].value_counts())

print("Impact of winning the toss on each team's performance:")
print(toss_impact.to_string(header=None))
