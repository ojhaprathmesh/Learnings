import pandas as pd
import matplotlib.pyplot as plt

countries = ["United States", "Canada", "United Kingdom"]

data = pd.read_csv("Olympic_medals.csv", encoding='latin1')

temp = data[data['Year'].apply(lambda x: 1996 <= x <= 2008)]

events = ["Hockey", "Football"]
fl_data = temp[temp['Country'].isin(countries) & temp['Sport'].isin(events)]

medal_counts = fl_data.groupby(['Country', 'Medal']).size().unstack(fill_value=0)

plt.figure(figsize=(10, 6))

medal_types = ["Gold", "Silver", "Bronze"]

for medal_type in medal_types:
    for country in countries:
        years = list(fl_data["Year"].drop_duplicates())
        medal_count_per_year = [0] * len(years)

        for index, year in enumerate(years):
            medal_count_per_year[index] = len(
                fl_data[(fl_data["Year"] == year) &
                        (fl_data["Country"] == country) &
                        (fl_data["Medal"] == medal_type)])

        plt.plot(years, medal_count_per_year, label=f"{country} - {medal_type}")

plt.xlabel("Year")
plt.ylabel("Total Number Of Medals")
plt.title("Time Series for Hockey and Football Medals")
plt.legend()
plt.show()
