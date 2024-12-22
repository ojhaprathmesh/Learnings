import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Define the Lorentz equations
def lorentz_equations(t, xyz, sigma, rho, beta):
    x, y, z = xyz
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

# Set the parameters for the Lorenz system
sigma = 10.0
rho = 28.0
beta = 8/3.0

# Define the time span for integration
t_span = (0, 50)
t_eval = np.linspace(*t_span, 10000)

# Set the initial conditions [x0, y0, z0]
initial_conditions = [1.0, 0.0, 0.0]

# Solve the Lorenz equations using SciPy's solve_ivp
solution = solve_ivp(lorentz_equations, t_span, initial_conditions, t_eval=t_eval, args=(sigma, rho, beta))

# Extract the solution
x, y, z = solution.y

# Plot the Lorenz attractor
plt.figure(figsize=(10, 8))
plt.plot(x, z, lw=0.5)
plt.title("Lorentz Attractor")
plt.xlabel("x")
plt.ylabel("z")
plt.show()
