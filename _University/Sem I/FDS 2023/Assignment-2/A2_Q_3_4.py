import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("StudentsPerformance.csv")

plt.figure(figsize=(10, 6))

# Male students
plt.subplot(1, 2, 1)
plt.hist(data[data["gender"] == "male"]["reading score"], edgecolor="black", bins=10)
plt.xlabel("Reading Score")
plt.ylabel("Frequency")
plt.title("Reading Scores of Male Students")

# Female students
plt.subplot(1, 2, 2)
plt.hist(data[data["gender"] == "female"]["reading score"], edgecolor="black", bins=10)
plt.xlabel("Reading Score")
plt.ylabel("Frequency")
plt.title("Reading Scores of Female Students")

plt.tight_layout()
plt.show()

