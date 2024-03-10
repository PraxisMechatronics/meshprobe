import csv
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import RegularGridInterpolator
from matplotlib.widgets import Slider, Button, CheckButtons, Cursor


def openfile():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename()  # Open file dialog
    if file_path:
        return file_path


def update_scale_value(val):
    global scale_value
    scale_value = val
    ax.set_box_aspect([data.shape[1], data.shape[0], scale_value])
    ax2.set_box_aspect([data.shape[1], data.shape[0], scale_value])
    plt.draw()


data = np.genfromtxt(openfile(), delimiter=",", skip_header=1)
print("raw data:")
print(data)

# generate grid upon which z values are mapped
x, y = np.linspace(0, data.shape[1], data.shape[1]), np.linspace(
    0, data.shape[0], data.shape[0]
)

xg, yg = np.meshgrid(x, y, indexing="xy")

interp = RegularGridInterpolator(
    (x, y),
    data.T,
    method="linear",
    bounds_error=False,
)

scale_value = 2
xx, yy = np.meshgrid(
    np.linspace(0, data.shape[1], int((data.shape[1] * 100))),
    np.linspace(0, data.shape[0], int((data.shape[0] * 100))),
    indexing="xy",
)

fig = plt.figure(figsize=(20, 10))
ax = fig.add_subplot(121, projection="3d")
ax.plot_surface(xx, yy, interp((xx, yy)), cmap=cm.coolwarm)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_box_aspect([data.shape[1], data.shape[0], scale_value])

ax2 = fig.add_subplot(122, projection="3d")
ax2.plot_surface(xg, yg, data, cmap=cm.coolwarm, linewidth=2, antialiased=True)
ax2.set_xlabel("x")
ax2.set_ylabel("y")
ax2.set_zlabel("z")
ax2.set_box_aspect([data.shape[1], data.shape[0], scale_value])

for n in [ax, ax2]:
    n.set_xlim(0, data.shape[1])
    n.set_ylim(0, data.shape[0])
    n.set_zlim(0, np.amax(data, axis=None))

# Create slider
slider_ax = plt.axes([0.1, 0.05, 0.8, 0.03])
c_slider = Slider(slider_ax, "Z axis exaggeration", 2, 12, valinit=2)
c_slider.on_changed(update_scale_value)

# Create Checkbuttons
rax = plt.axes([0.05, 0.1, 0.12, 0.05])
check = CheckButtons(
    rax, ("Show generated plot", "Show interpolated plot"), (False, True)
)


plt.show()
