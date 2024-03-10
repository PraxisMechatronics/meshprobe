import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Create figure and axis
fig = plt.figure(figsize=(8, 4))  # Adjust the figure size as needed
ax = fig.add_subplot(111, projection="3d")

# Generate data
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

# Plot 3D surface
ax.plot_surface(X, Y, Z, cmap="viridis")

# Set labels
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

plt.show()
