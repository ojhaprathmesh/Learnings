import pandas as pd

data = pd.read_csv("Olympic_medals.csv", encoding='latin1')

data['Participation'] = data.groupby(['Year', 'Sport']).transform('size')

max_participation = data.groupby(['Year', 'Sport'])['Participation'].max().reset_index()

max_row = max_participation.loc[max_participation['Participation'].idxmax()]

result_format = (f"Maximum participation ever made was of {max_row['Participation']} "
                 f"in the {max_row['Sport']} sport in the year {max_row['Year']}")

print(result_format)

