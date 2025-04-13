import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle
import numpy as np

# Define ellipse parameters
center = (0, 0)  # (h, k) - center of the ellipse
width = 4         # 2a - length of the major axis
height = 2        # 2b - length of the minor axis
angle = 0         # Rotation angle in degrees

# Create figure and axis
fig, ax = plt.subplots()

# Create ellipse
ellipse = Ellipse(center, width, height, angle=angle, edgecolor='b', facecolor='none')
circle = Circle(center, 1, edgecolor='r', facecolor='none')
# Add the ellipse to the plot
ax.add_patch(ellipse)
ax.add_patch(circle)

# Set aspect ratio to 'equal' to make sure the ellipse is drawn correctly
ax.set_aspect('equal', adjustable='box')

# Set axis limits with additional space around the ellipse
padding = 1.0  # adjust this value to control the space around the ellipse
ax.set_xlim(-width / 2 - padding, width / 2 + padding)
ax.set_ylim(-height / 2 - padding, height / 2 + padding)

# Set labels and title
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_title('Ellipse Plot')

# Show the plot
plt.show()
