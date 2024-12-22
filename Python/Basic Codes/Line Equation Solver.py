import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-5, 5, 100)
y = x**2

plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Quadratic Equation')

# Set the origin at (0, 0)
plt.xlim(-5, 5)
plt.ylim(0, 25)

plt.axhline(0, color='black', linewidth=0.5)  # Horizontal line at y=0
plt.axvline(0, color='black', linewidth=0.5)  # Vertical line at x=0

plt.grid(True)
plt.show()