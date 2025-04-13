import pandas as pd

data = pd.read_csv('IPL Matches 2008-2020.csv')
most_player_of_match = data['player_of_match'
                            ].value_counts().head(1).to_string(header=None)

player_name = most_player_of_match.split('  ')[0]
awards = most_player_of_match.split('  ')[2]

print(f"Player with the most player of the match awards: "
      f"{player_name} --> {awards}")

