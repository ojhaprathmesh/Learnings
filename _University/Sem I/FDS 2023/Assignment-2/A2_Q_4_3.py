import pandas as pd

df = pd.read_csv('IPL Ball-by-Ball 2008-2020.csv')

reliable_batsmen_by_team = df.groupby('batting_team')['batsman'].value_counts().groupby(level=0).head(1)
reliable_bowlers_by_team = df.groupby('bowling_team')['bowler'].value_counts().groupby(level=0).head(1)
most_reliable_batsman_in_league = df['batsman'].value_counts().head(1).to_string(header=None)
most_reliable_bowler_in_league = df['bowler'].value_counts().head(1).to_string(header=None)

print('\nMost reliable batsmen in each team:')
for team, reliable_batsmen in reliable_batsmen_by_team.keys():
    print(f'\t{team}: {reliable_batsmen}')

print('\nMost reliable bowlers in each team:')
for team, reliable_bowlers in reliable_bowlers_by_team.keys():
    print(f'\t{team}: {reliable_bowlers}')

print(f"\nMost reliable batsmen in league is {most_reliable_batsman_in_league.split('  ')[0]}")
print(f"\nMost reliable bowler in league is {most_reliable_bowler_in_league.split('  ')[0]}")

