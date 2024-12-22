import pandas as pd

'''
Apparently I found that csv file is not in correct encoding so to open and
read the file correctly argument encoding='latin1' needs to be passed
'''
data = pd.read_csv("Olympic_medals.csv", encoding='latin1')

gold_men = 0
gold_women = 0

'''
Since zip() is an unusual function, here is it's use:
It combines 2 or more iterables into one iterables
'''

for gender, medal in zip(data["Event_gender"], data["Medal"]):
    if medal == 'Gold':
        if gender == 'M':
            gold_men += 1
        else:
            gold_women += 1
print(f"Gold medals won by men : {gold_men}")
print(f"Gold medals won by women : {gold_women}")
