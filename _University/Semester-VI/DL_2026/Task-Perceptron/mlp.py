"""
PART 2 — Multi-Layer Perceptron (MLP) from First Principles
Dataset : XOR Gate
Tools   : NumPy only
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons

matplotlib.use("Agg")

# Generate dataset
X, y = make_moons(
    n_samples=500,
    noise=0.2,
    random_state=42
)
np.random.seed(42)


def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def sigmoid_derivative(z):
    s = sigmoid(z)
    return s * (1 - s)

def bce_loss(y, y_hat):
    return -np.mean(
        y*np.log(y_hat + 1e-9) +
        (1-y)*np.log(1-y_hat + 1e-9)
    )


class MLP:

    def __init__(self, n_input, n_hidden, n_output, lr=0.1):

        self.lr = lr

        self.W1 = np.random.randn(n_input, n_hidden) * 0.5
        self.b1 = np.zeros(n_hidden)

        self.W2 = np.random.randn(n_hidden, n_output) * 0.5
        self.b2 = np.zeros(n_output)

    def forward(self, X):

        self.Z1 = X @ self.W1 + self.b1
        self.A1 = sigmoid(self.Z1)

        self.Z2 = self.A1 @ self.W2 + self.b2
        self.A2 = sigmoid(self.Z2)

        return self.A2

    def backward(self, X, y):

        m = X.shape[0]
        y = y.reshape(-1,1)

        dZ2 = self.A2 - y
        dW2 = self.A1.T @ dZ2 / m
        db2 = dZ2.mean(axis=0)

        dA1 = dZ2 @ self.W2.T
        dZ1 = dA1 * sigmoid_derivative(self.Z1)

        dW1 = X.T @ dZ1 / m
        db1 = dZ1.mean(axis=0)

        self.W2 -= self.lr * dW2
        self.b2 -= self.lr * db2
        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1

    def fit(self, X, y, epochs=5000):

        self.losses = []

        for _ in range(epochs):

            y_hat = self.forward(X)
            self.backward(X, y)

            loss = bce_loss(y, y_hat.ravel())
            self.losses.append(loss)

    def predict(self, X):

        return (self.forward(X).ravel() >= 0.5).astype(int)

    def score(self, X, y):

        return np.mean(self.predict(X) == y)


# XOR Dataset
X = np.array([
    [0,0],
    [0,1],
    [1,0],
    [1,1]
], dtype=float)

y = np.array([0,1,1,0])


mlp = MLP(n_input=2, n_hidden=4, n_output=1, lr=0.5)
mlp.fit(X, y, epochs=5000)


print("="*40)
print("MLP — XOR Gate")
print("="*40)

print("Predictions:", mlp.predict(X))
print("Accuracy:", mlp.score(X,y)*100, "%")
print("Final Loss:", mlp.losses[-1])


# Plot loss curve
plt.figure(figsize=(6,4))
plt.plot(mlp.losses)
plt.title("MLP Training Loss")
plt.xlabel("Epoch")
plt.ylabel("Binary Cross Entropy")
plt.grid(True)

plt.savefig("mlp_training_loss.png")
plt.close()

print("Plot saved -> mlp_training_loss.png")