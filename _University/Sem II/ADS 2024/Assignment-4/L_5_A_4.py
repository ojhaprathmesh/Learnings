import pandas as pd
import matplotlib.pyplot as plt
from numpy import linspace, exp, sqrt, pi

df = pd.read_excel("StudentsPerformance.xlsx")

# Q1
female_data = df[df["gender"] == "female"]

print(f"Number of female students: {female_data.shape[0]}\n")

# Q2
groups = df["group"].sort_values().unique()

for group in groups:
    male_count = df[(df["gender"] == "male") & (df["group"] == group)].shape[0]
    print(f"Number of male students in {group}: {male_count}")

# Q3
female_std_lunch_count = female_data[female_data["lunch"] == "standard"].shape[0]
print(f"Number of female students having standard lunch: {female_std_lunch_count}\n")

# Q4
male_data = df[df["gender"] == "male"]
male_score_count = male_data[male_data["reading score"] > 70].shape[0]
print(f"Number of male students with reading score more than 70 : {male_score_count}\n")

# Q5
female_score_count = female_data[female_data["reading score"] < 70].shape[0]
print(f"Number of female students with reading score less than 70 : {female_score_count}\n")

# ======== Some Other Questions ========

# Bar Plot
req_df = df[df["reading score"] > 60]

education_counts = req_df["parental level of education"].value_counts()

plt.figure(figsize=(10, 6))
education_counts.plot(kind="bar", color="skyblue")
plt.xlabel("Parental Level of Education")
plt.ylabel("Number of Students")
plt.title("Number of Students with Reading Score > 60 by Parental Education Level")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Gaussian Distribution
math_scores = df["math score"]

mean_score = math_scores.mean()
median_score = math_scores.median()
mode_score = math_scores.mode().values[0]

plt.figure(figsize=(10, 6))
x_min = math_scores.min()
x_max = math_scores.max()
x = linspace(x_min, x_max, 100)
p = (1 / (sqrt(2 * pi) * math_scores.std())) * exp(-0.5 * ((x - math_scores.mean()) / math_scores.std()) ** 2)
plt.plot(x, p, "k", linewidth=2)

plt.axvline(mean_score, color="red", linestyle="dashed", linewidth=1, label=f"Mean: {mean_score:.2f}")
plt.axvline(median_score, color="green", linestyle="dashed", linewidth=1, label=f"Median: {median_score}")
plt.axvline(mode_score, color="purple", linestyle="dashed", linewidth=1, label=f"Mode: {mode_score}")

plt.xlabel("Math Score")
plt.ylabel("Density")
plt.title("Gaussian Distribution of Students\" Math Scores")
plt.legend()
plt.show()

# Bar Plot
grouped = df.groupby(["test preparation course", "group"]).size().unstack()
grouped.plot(kind="bar", stacked=True)
plt.xlabel("Group")
plt.ylabel("Number of Students")
plt.title("Number of Students by Test Preparation Course and Group")
plt.legend(title="Test Preparation Course")
plt.xticks(rotation=0)
plt.show()

# Analysis
male_standard_mean = male_data[male_data['lunch'] == 'standard']['math score'].mean()
male_free_mean = male_data[male_data['lunch'] == 'free/reduced']['math score'].mean()

female_standard_mean = female_data[female_data['lunch'] == 'standard']['math score'].mean()
female_free_mean = female_data[female_data['lunch'] == 'free/reduced']['math score'].mean()

print("Mean math score for male students with standard lunch:", male_standard_mean)
print("Mean math score for male students with free lunch:", male_free_mean)
print("Mean math score for female students with standard lunch:", female_standard_mean)
print("Mean math score for female students with free lunch:", female_free_mean)

plt.figure(figsize=(10, 6))
plt.bar(['Standard Lunch (Male)', 'Free Lunch (Male)', 'Standard Lunch (Female)', 'Free Lunch (Female)'],
        [male_standard_mean, male_free_mean, female_standard_mean, female_free_mean],
        color=['blue', 'orange', 'green', 'red'])
plt.xlabel('Group')
plt.ylabel('Mean Math Score')
plt.title('Mean Math Score by Gender and Lunch Type')
plt.show()
