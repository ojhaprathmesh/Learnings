import pandas as pd
import matplotlib.pyplot as plt

countries = ["United States", "Canada", "United Kingdom"]

data = pd.read_csv("Olympic_medals.csv", encoding='latin1')

temp = data[data["Year"].apply(lambda x: 1996 <= x <= 2008)]

fl_data = temp[temp["Country"].apply(lambda x: x in countries)]

plt.figure(figsize=(10, 6))

for country in countries:
    years = list(fl_data["Year"].drop_duplicates())
    medal_count_per_year = [0] * len(years)

    for index, year in enumerate(years):
        medal_count_per_year[index] = len(
            fl_data[(fl_data["Year"] == year) & (fl_data["Country"] == country)]
        )

    plt.plot(years, medal_count_per_year, label=country)

plt.xlabel("Year")
plt.ylabel("Total Number Of Medals")
plt.title("Time Series")
plt.legend()
plt.show()
