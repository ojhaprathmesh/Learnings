import numpy as np

# Define the function f(x)
def f(x):
    return np.sqrt(25 - x**2)

# Trapezoidal rule function
def trapezoidal_rule(f, a, b, h):
    x = np.arange(a, b + h, h)
    y = f(x)
    return h * (0.5 * y[0] + np.sum(y[1:-1]) + 0.5 * y[-1])

# Exact AUC (quarter-circle area)
exact_AUC = (1/4) * np.pi * (5**2)  # Quarter of a circle with radius 5

# Initialize h and store results
h_values = [1.0]
results = []

while h_values[-1] >= 0.01:  # Reduce h until it reaches 0.01
    h = h_values[-1]
    approx_AUC = trapezoidal_rule(f, 0, 5, h)
    error = abs(exact_AUC - approx_AUC)
    results.append((h, approx_AUC, error))
    h_values.append(h / 2)  # Reduce h by half each iteration

# Save results to a file
with open("auc_results.txt", "w") as file:
    file.write("h\tApprox_AUC\tError\n")
    for h, approx_AUC, error in results:
        file.write(f"{h:.5f}\t{approx_AUC:.5f}\t{error:.5f}\n")

print("Results saved to auc_results.txt")
