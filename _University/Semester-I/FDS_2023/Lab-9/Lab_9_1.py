import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

plt.plot(x, y, label='y = sin(x)', linestyle='-', marker='o', markevery=[0, 25, 50, 75])

plt.xlabel('x')
plt.ylabel('sin(x)')

plt.xticks(np.arange(0, 2 * np.pi + np.pi / 2, np.pi / 2), ['0', '$\pi/2$', '$\pi$', '$3\pi/2$', '$2\pi$'])

plt.legend()
plt.show()
