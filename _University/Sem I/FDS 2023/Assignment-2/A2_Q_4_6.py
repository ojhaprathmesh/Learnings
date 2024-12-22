import pandas as pd

data = pd.read_csv('IPL Ball-by-Ball 2008-2020.csv')
pdm = data.groupby(['batting_team', 'dismissal_kind']
                   ).size().groupby(level=0).idxmax()

for team, dismissal in pdm:
    print(f"Team: {team} || Dismissal Method: {dismissal}")

