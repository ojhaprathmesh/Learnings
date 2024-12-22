from sklearn.cluster import KMeans
import pandas as pd

df = pd.read_csv("Mall_Customers.csv")

features = ['Annual Income (k$)', 'Spending Score (1-100)']

X = df[features].values

n = 3  # Number of clusters

kmeans = KMeans(n_clusters=n)
kmeans.fit(X)

cluster_labels = kmeans.labels_

centroids = kmeans.cluster_centers_

df['Cluster'] = cluster_labels

print(f"Cluster Centroids: {centroids}")

print(f"Number of data points in each cluster: {df['Cluster'].value_counts()}")
