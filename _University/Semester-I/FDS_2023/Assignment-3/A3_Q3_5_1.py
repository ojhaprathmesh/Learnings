import matplotlib.pyplot as plt
import seaborn as sns

data = [12, 15, 18, 22, 26, 29, 35, 42, 50, 100]

# Create a boxplot
sns.boxplot(x=data)
plt.show()
