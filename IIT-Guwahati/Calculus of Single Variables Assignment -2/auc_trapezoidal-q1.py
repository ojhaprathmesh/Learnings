import numpy as np


def f(x):
    return np.sqrt(25 - x ** 2)


def trapezoidal_rule(a, b, h):
    n = int((b - a) / h)
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return (h / 2) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])


# Exact AUC (Area of a quarter-circle with radius 5)
A_exact = (np.pi * 25) / 4

# File to store results
output_file = "auc_results.txt"
with open(output_file, "w") as file:
    file.write("h, A_hat(h), Error\n")

    h = 1.0  # Initial step size
    factor = 2  # Reduction factor
    while h > 1e-4:
        A_hat = trapezoidal_rule(0, 5, h)
        error = abs(A_exact - A_hat)
        file.write(f"{h}, {A_hat}, {error}\n")
        h /= factor  # Reduce step size

print(f"Results saved in {output_file}")
