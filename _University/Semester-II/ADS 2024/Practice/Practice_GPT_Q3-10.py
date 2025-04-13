import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

df = pd.read_csv("Mall_Customers.csv")

features = ['Annual Income (k$)', 'Spending Score (1-100)']
X = df[features].values

# Creating and fitting the KMeans model
kmeans = KMeans(n_clusters=3)
kmeans.fit(X)

# Getting cluster labels for each data point
labels = kmeans.labels_

# Getting centroid coordinates
centroids = kmeans.cluster_centers_

# Plotting the clusters
plt.figure(figsize=(8, 6))
scatter = plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', edgecolors='k')
plt.scatter(centroids[:, 0], centroids[:, 1], marker='X', s=200, color='red', label='Centroids')
plt.xlabel('Annual Income')
plt.ylabel('Spending Score')
plt.title('Clusters Formed by KMeans Algorithm')
plt.colorbar(scatter, label='Cluster')
plt.legend()
plt.grid(True)
plt.show()
