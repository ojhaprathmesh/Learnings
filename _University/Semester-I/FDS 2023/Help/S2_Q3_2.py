import pandas as pd

# load the datasets
df15 = pd.read_csv('https://raw.githubusercontent.com/hirdeshiitkgp/Data/main/2015_rankings.csv')

print(f"{df15["scores_international_outlook"].max()}")
