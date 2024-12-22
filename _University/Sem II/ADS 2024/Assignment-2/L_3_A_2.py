import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("CSS.csv").dropna().drop_duplicates()

# Group by publication year and count the number of publications for each year
publications_by_year = df.groupby('Pub_Year').size()

# Line plot
# plt.figure(figsize=(10, 6))
publications_by_year.plot(kind='line', marker='o', color='skyblue', linewidth=2)
plt.title('Number of Publications Over Publication Years')
plt.xlabel('Publication Year')
plt.ylabel('Number of Publications')
plt.yscale('log')
plt.xticks(range(publications_by_year.index.min(), publications_by_year.index.max(), 2),
           rotation=45)  # Rotate x-axis labels for better readability
plt.grid(True)
plt.show()

# Box plot
plt.figure(figsize=(10, 6))
req = df[(df['Pub_Year'] >= 2001) & (df['Pub_Year'] <= 2023)]
plt.boxplot([req[req['Pub_Year'] == year]['Citations'] for year in req['Pub_Year'].unique()],
            labels=req['Pub_Year'].unique(), showfliers=True, flierprops=dict(marker='D', markersize=8,
                                                                              markerfacecolor='black'))
plt.title('Box Plot of Citations Received by Publication Year')
plt.xlabel('Publication Year')
plt.ylabel('Citations Received')
plt.yscale('log')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.show()

# Bar plot for document types
plt.figure(figsize=(10, 6))
document_type_counts = df['Document Type'].value_counts()
document_type_counts.plot(kind='bar', color='skyblue')
plt.title('Bar Plot of Publication Types')
plt.xlabel('Document Type')
plt.ylabel('Count')
plt.yscale('log')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.show()

# Bar plot for languages
plt.figure(figsize=(10, 6))
language_counts = df['Language'].value_counts()
language_counts.plot(kind='bar', color='skyblue')
plt.title('Bar Plot Of Language Types')
plt.xlabel('Language')
plt.ylabel('Count')
plt.yscale('log')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.show()

# Scatter Plot
df["Auth_Num"] = df["Author_Name"].str.split(";").apply(len)
publications_by_authors = df.groupby('Auth_Num').size()

# Line plot for number of publications vs. number of authors
plt.figure(figsize=(10, 6))
publications_by_authors.plot(kind='line', marker='o', color='skyblue', linewidth=2)
plt.title('Number of Publications vs. Number of Authors')
plt.xlabel('Number of Authors')
plt.ylabel('Number of Publications')
plt.grid(True)  # Add gridlines for better readability
plt.show()
