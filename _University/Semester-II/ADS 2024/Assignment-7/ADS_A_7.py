import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("Example_Pivot_Project.xlsx")

# Create a pivot table
pivot_table = pd.pivot_table(df, values='Order Amount', index='Salesperson', columns='Month', aggfunc='sum')

# Plot the pivot table
pivot_table.plot(kind='bar', figsize=(10, 6))
plt.title('Order Amount by Salesperson and Month')
plt.xlabel('Salesperson')
plt.ylabel('Order Amount')
plt.xticks(rotation=45)
plt.legend(title='Month')
plt.tight_layout()
plt.show()

total_amount_william_davis = df["Order Amount"][df["Salesperson"] == "Davis, William"]

total_amount_march = df["Order Amount"][df["Month"] == "March"]

salesperson = ("Albertson, Kathy", "Brennan, Micheal")
grand_total = df.loc[df["Salesperson"].isin(salesperson), "Order Amount"]

summary = pd.pivot_table(data=df, index="Region", columns="Month", values="Order Amount", aggfunc='sum')

print(f"Total amount ordered by William Davis: "
      f"{total_amount_william_davis.size} units costing $"
      f"{total_amount_william_davis.sum()}")

print(f"Total amount ordered by all: "
      f"{total_amount_march.size} units costing $"
      f"{total_amount_march.sum()}")

print(summary)

print(f"Grand total amount ordered by Kathy Albertson and Micheal Brennan: "
      f"{grand_total.size} units costing $"
      f"{grand_total.sum()}")
