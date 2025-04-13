import pandas as pd

df = pd.read_csv('IPL Matches 2008-2020.csv')
matches = df['team1'].value_counts() + df['team2'].value_counts()
wins = df['winner'].value_counts()
win_percent_each_team = (wins / matches) * 100

for team, win_percentage in win_percent_each_team.items():
    print(f"{team}: {win_percentage:.2f}%")
