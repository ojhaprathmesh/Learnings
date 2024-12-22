from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng()
Column1 = rng.normal(size=150)
Column2 = rng.normal(size=150)

# Making a dataframe using pandas of column1 and column2
df = pd.DataFrame({
    "Column1": Column1,
    "Column2": Column2
})

# Taking values in X to apply Kmeans

X = df[['Column1', 'Column2']].values

n = 3  # Number of clusters

kmeans = KMeans(n_clusters=n)
kmeans.fit(X)

cluster_labels = kmeans.labels_

centroids = kmeans.cluster_centers_

df['Cluster'] = cluster_labels

print(f"Cluster Centroids: {centroids}")

print(f"Number of data points in each cluster: {df['Cluster'].value_counts()}")

# Plotting the clusters
plt.figure(figsize=(8, 6))
scatter = plt.scatter(X[:, 0], X[:, 1], c=cluster_labels, cmap='viridis', edgecolors='k')
plt.scatter(centroids[:, 0], centroids[:, 1], marker='X', s=200, color='red', label='Centroids')
plt.xlabel('Annual Income')
plt.ylabel('Spending Score')
plt.title('Clusters Formed by KMeans Algorithm')
plt.colorbar(scatter, label='Cluster')
plt.legend()
plt.grid(True)
plt.show()
