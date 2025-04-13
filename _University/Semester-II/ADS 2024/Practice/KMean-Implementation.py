import numpy as np


def kmeans(X, n_clusters, max_iter=300):
    # Initialize centroids randomly
    centroids = X[np.random.choice(X.shape[0], n_clusters, replace=False)]

    for _ in range(max_iter):
        # Assign each data point to the nearest centroid
        labels = np.argmin(((X[:, np.newaxis] - centroids) ** 2).sum(axis=2), axis=1)

        # Update centroids by taking the mean of all data points assigned to each cluster
        new_centroids = np.array([X[labels == k].mean(axis=0) for k in range(n_clusters)])

        # If centroids stop changing, break the loop
        if np.all(centroids == new_centroids):
            break

        centroids = new_centroids

    return centroids, labels


# Example usage
# Generate random data
np.random.seed(42)
X = np.random.randn(100, 2)

# Apply KMeans algorithm
centroids, labels = kmeans(X, n_clusters=3)

print("Centroids:", centroids)
print("Labels:", labels)
