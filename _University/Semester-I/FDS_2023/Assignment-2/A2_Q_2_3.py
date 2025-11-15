import pandas as pd
import matplotlib.pyplot as plt

iris_df = pd.read_csv('iris-data.csv')

plt.figure(figsize=(12, 5))

plt.subplot(1, 3, 1)
plt.scatter(iris_df['sepal length'], iris_df['sepal width'], c='b')
plt.title('Sepal Length vs. Sepal Width')
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')
plt.ylim(0, 7)

plt.subplot(1, 3, 2)
plt.scatter(iris_df['sepal length'], iris_df['petal length'], c='g')
plt.title('Sepal Length vs. Petal Length')
plt.xlabel('Sepal Length')
plt.ylabel('Petal Length')
plt.ylim(0, 7)

plt.subplot(1, 3, 3)
plt.scatter(iris_df['sepal length'], iris_df['petal width'], c='r')
plt.title('Sepal Length vs. Petal Width')
plt.xlabel('Sepal Length')
plt.ylabel('Petal Width')
plt.ylim(0, 7)

plt.tight_layout()
plt.show()

