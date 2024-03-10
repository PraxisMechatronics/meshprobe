import csv
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import RegularGridInterpolator
from matplotlib.widgets import (
    Slider,
    Button,
    CheckButtons,
    MultiCursor,
    TextBox,
    RadioButtons,
)


def openfile():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename()  # Open file dialog
    if file_path:
        return file_path


def update_scale_value(val):
    # global scale_value
    scale_value = val
    ax.set_box_aspect([data.shape[1], data.shape[0], scale_value])
    ax2.set_box_aspect([data.shape[1], data.shape[0], scale_value])
    plt.draw()


def update_visibility(label):
    if label == "Show generated plot":
        ax2.set_visible(not ax2.get_visible())
    elif label == "Show interpolated plot":
        ax.set_visible(not ax.get_visible())
    plt.draw()


def interp_method(label):
    global interp_method_, interp
    interp_method_ = label
    interp = RegularGridInterpolator(
        (x, y),
        data.T,
        method=interp_method_,
        bounds_error=False,
    )
    ax.cla()
    ax.plot_surface(xx, yy, interp((xx, yy)), cmap=cm.plasma)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_box_aspect([data.shape[1], data.shape[0], scale_value])
    plt.draw()


def update_mult_value(val):
    global mult_value, xx, yy
    mult_value = int(val)
    xx, yy = np.meshgrid(
        np.linspace(0, data.shape[1], int(data.shape[1] * mult_value)),
        np.linspace(0, data.shape[0], int(data.shape[0] * mult_value)),
        indexing="xy",
    )
    ax.cla()
    ax.plot_surface(xx, yy, interp((xx, yy)), cmap=cm.plasma)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_box_aspect([data.shape[1], data.shape[0], scale_value])
    plt.draw()


"""data = np.genfromtxt(openfile(), delimiter=",", skip_header=1)
print("raw data:")
print(data)"""
file_path = openfile()
with open(file_path, "r") as file:
    num_rows = int(file.readline().strip())
    num_cols = int(file.readline().strip())
data = np.genfromtxt(file_path, skip_header=2)
data = data.reshape(num_rows, num_cols)
print(data)

# generate grid upon which z values are mapped
x, y = np.linspace(0, data.shape[1], data.shape[1]), np.linspace(
    0, data.shape[0], data.shape[0]
)

xg, yg = np.meshgrid(x, y, indexing="xy")

interp_method_ = "nearest"

interp = RegularGridInterpolator(
    (x, y),
    data.T,
    method=interp_method_,
    bounds_error=False,
)

global scale_value
scale_value = 2

mult_value = 10
xx, yy = np.meshgrid(
    np.linspace(0, data.shape[1], int((data.shape[1] * int(mult_value)))),
    np.linspace(0, data.shape[0], int((data.shape[0] * int(mult_value)))),
    indexing="xy",
)

fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(121, projection="3d")
ax.plot_surface(xx, yy, interp((xx, yy)), cmap=cm.plasma)
ax.set_title("Interpolated Plot")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_box_aspect([data.shape[1], data.shape[0], scale_value])

ax2 = fig.add_subplot(122, projection="3d")
surf = ax2.plot_surface(xg, yg, data, cmap=cm.plasma, linewidth=2, antialiased=True)
ax2.set_title("Raw Data Generated Plot")
ax2.set_xlabel("x")
ax2.set_ylabel("y")
ax2.set_zlabel("z")
ax2.set_box_aspect([data.shape[1], data.shape[0], scale_value])

for n in [ax, ax2]:
    n.set_xlim(0, data.shape[1])
    n.set_ylim(0, data.shape[0])
    n.set_zlim(np.amin(data, axis=None), np.amax(data, axis=None))

# Create slider
slider_ax = plt.axes([0.1, 0.05, 0.8, 0.03])
c_slider = Slider(slider_ax, "Z axis exaggeration", 2, 12, valinit=2)
c_slider.on_changed(update_scale_value)

slider2_ax = plt.axes([0.1, 0.02, 0.8, 0.03])
mult_slider = Slider(slider2_ax, "Interpolation Multiplier", 1, 50, valinit=10)
mult_slider.on_changed(update_mult_value)

# Create Checkbuttons
rax = plt.axes([0.05, 0.1, 0.12, 0.05])
check_plots = CheckButtons(
    rax, ("Show generated plot", "Show interpolated plot"), (True, True)
)
check_plots.on_clicked(update_visibility)

radio_background = "lightgoldenrodyellow"
pax = plt.axes([0.05, 0.15, 0.12, 0.05])
radio = RadioButtons(
    pax,
    ("nearest", "linear", "cubic", "quintic"),
)
radio.on_clicked(interp_method)

fig.colorbar(surf, ax=[ax, ax2], shrink=0.5, aspect=50)
fig.text(0.5, 0.95, "Table Flatness Mesh Probe Interpreter", fontsize=34, ha="center")
plt.show()
