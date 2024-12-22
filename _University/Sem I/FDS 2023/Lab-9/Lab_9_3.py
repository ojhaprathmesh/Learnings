import matplotlib.pyplot as plt
import numpy as np

# Number of random points to plot
num_points = 10

# Create figure and axis
fig, ax = plt.subplots()

# Plot random points with triangles of increasing size
x_points = np.random.rand(num_points)
y_points = np.random.rand(num_points)

# Set aspect ratio to 'equal' to make sure the triangles are drawn correctly
ax.set_aspect('equal', adjustable='box')

# Set limits of the axes to keep the size the same
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Plot each point individually with its corresponding size
for x, y in zip(x_points, y_points):
    markersize = 5 + 2.5 * x
    ax.plot(x, y, marker='^', linestyle=' ', color='b', markersize=markersize)

# Set labels and title
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_title('Random Points with Size Increasing along X-axis')

# Show the plot
plt.show()
