import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("Olympic_medals.csv", encoding='latin1')

selected_games = ["Aquatics", "Athletics", "Equestrians", "Football"]
selected_data = data[data['Sport'].isin(selected_games)]
gender_counts = selected_data['Gender'].value_counts()

plt.figure(figsize=(10, 6))
gender_counts.plot(kind='bar', color=['blue', 'pink'])
plt.xlabel("Gender")
plt.ylabel("Number of Participants")
plt.title("Male and Female Participation in Selected Games")
plt.xticks(rotation=0)
plt.show()

selected_years_data = data[data['Year'].apply(lambda x: 1976 <= x <= 2000)]
selected_sports = ["Football", "Hockey", "Aquatics", "Athletics", "Basketball"]
selected_sports_data = selected_years_data[selected_years_data['Sport'].isin(selected_sports)]

dominant_countries = {}
for sport in selected_sports:
    sport_data = selected_sports_data[selected_sports_data['Sport'] == sport]
    top_country = sport_data[sport_data['Medal'] == 'Gold']['Country'].value_counts().idxmax()
    dominant_countries[sport] = top_country

print("Dominant Countries:")
for sport, country in dominant_countries.items():
    print(f"{sport}: {country}")


