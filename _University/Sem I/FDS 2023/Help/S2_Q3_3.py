import pandas as pd

# load the datasets
df15 = pd.read_csv('https://raw.githubusercontent.com/hirdeshiitkgp/Data/main/2015_rankings.csv')

print(df15[df15["location"] == 'United States'])
