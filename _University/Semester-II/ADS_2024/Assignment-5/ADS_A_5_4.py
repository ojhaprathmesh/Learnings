import pandas as pd
import cufflinks as cf
import plotly.express as px

df = pd.read_csv("IRIS.csv").drop_duplicates().dropna()

# Enable cufflinks offline mode
cf.go_offline()

# Interactive scatter plot using Plotly Express
fig = px.scatter(df, x='sepal_length', y='sepal_width', color='species', title='Interactive Scatter Plot')
fig.show()


# Built-in dataset
geo_df = px.data.gapminder()

# Choropleth map
fig = px.choropleth(geo_df, locations="iso_alpha", color="lifeExp", hover_name="country",
                    animation_frame="year", range_color=[20, 80],
                    title="Life Expectancy Over Time")
fig.show()
