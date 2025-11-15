import pandas as pd

data = pd.read_csv("Olympic_medals.csv", encoding='latin1')

gold_men = 0
gold_women = 0

for year, gender, medal in zip(data["Year"], data["Event_gender"], data["Medal"]):
    if year == 1976 and medal == 'Gold':
        if gender == 'M':
            gold_men += 1
        else:
            gold_women += 1

print(f"Gold medals won by men : {gold_men}")
print(f"Gold medals won by women : {gold_women}")
