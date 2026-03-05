"""
PART 1 — Single-Layer Perceptron (Binary Classification)
Dataset : AND Gate
Tools   : NumPy only
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs

matplotlib.use("Agg")
np.random.seed(42)

# Generate dataset
X, y = make_blobs(
    n_samples=500,
    centers=2,
    n_features=2,
    cluster_std=1.5,
    random_state=42
)

y = y.astype(int)


class Perceptron:
    def __init__(self, learning_rate=0.1, n_epochs=50):
        self.lr = learning_rate
        self.n_epochs = n_epochs
        self.weights = None
        self.bias = 0.0
        self.errors_ = []

    def predict(self, X):
        return np.where(X @ self.weights + self.bias >= 0, 1, 0)

    def fit(self, X, y):
        self.weights = np.zeros(X.shape[1])

        for _ in range(self.n_epochs):
            errors = 0

            for xi, yi in zip(X, y):
                prediction = self.predict(xi.reshape(1, -1))[0]
                delta = self.lr * (yi - prediction)

                self.weights += delta * xi
                self.bias += delta

                errors += int(delta != 0)

            self.errors_.append(errors)

    def score(self, X, y):
        return np.mean(self.predict(X) == y)


# AND gate dataset
X = np.array([
    [0,0],
    [0,1],
    [1,0],
    [1,1]
], dtype=float)

y = np.array([0,0,0,1])


p = Perceptron(learning_rate=0.1, n_epochs=10)
p.fit(X, y)

print("="*40)
print("Perceptron — AND Gate")
print("="*40)

print("Weights:", p.weights)
print("Bias:", p.bias)
print("Predictions:", p.predict(X))
print("Accuracy:", p.score(X,y)*100, "%")


# Plot errors per epoch
plt.figure(figsize=(6,4))
plt.plot(range(1,len(p.errors_)+1), p.errors_, marker="o")
plt.title("Perceptron Training Errors")
plt.xlabel("Epoch")
plt.ylabel("Misclassifications")
plt.grid(True)

plt.savefig("perceptron_training.png")
plt.close()

print("Plot saved -> perceptron_training.png")