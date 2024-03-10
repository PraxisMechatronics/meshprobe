import csv
import ctypes
import tkinter as tk
import numpy as np
import matplotlib as mpl
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
    root.title("test")
    file_path = filedialog.askopenfilename()  # Open file dialog
    if file_path:
        return file_path


def update_both_values(val):
    print(val)


def update_scale_value(val):
    # global scale_value
    scale_value = val
    ax.set_box_aspect([data.shape[1], data.shape[0], scale_value])
    plt.draw()


def interp_method(label):
    global interp_method_, interp
    interp_method_ = label
    if interp_method_ == "cubic" or interp_method_ == "quintic":
        mult_slider.set_val(1)
    interp = RegularGridInterpolator(
        (x, y),
        data.T,
        method=interp_method_,
        bounds_error=False,
    )
    ax.cla()
    # ax.set_title("Interpolated Plot")
    ax.plot_surface(xx, yy, interp((xx, yy)), cmap=cm.plasma)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    update_mult_value(mult_slider.val)


def update_mult_value(val):
    global mult_value, xx, yy, scale_value
    mult_value = int(val)
    xx, yy = np.meshgrid(
        np.linspace(0, data.shape[1], int(data.shape[1] * mult_value)),
        np.linspace(0, data.shape[0], int(data.shape[0] * mult_value)),
        indexing="xy",
    )
    ax.cla()
    ax.plot_surface(xx, yy, interp((xx, yy)), cmap=cm.plasma)
    # ax.set_title("Interpolated Plot")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    """ax.set_box_aspect([data.shape[1], data.shape[0], c_slider.val])"""
    plt.draw()


file_path = openfile()
with open(file_path, "r") as file:
    num_rows = int(file.readline().strip())
    num_cols = int(file.readline().strip())
data = np.genfromtxt(file_path, skip_header=2)
data = data.reshape(num_rows, num_cols)
print(data)


mpl.rcParams.update({"font.size": 18})

fig = plt.figure()  # figsize=(10, 5))
ax = fig.add_subplot(111, projection="3d")

# Create slider
slider_ax = plt.axes([0.1, 0.05, 0.8, 0.03])
scalemean = (data.shape[1] + data.shape[0]) / 4
c_slider = Slider(
    slider_ax,
    "Z scale",
    scalemean / 2,
    scalemean * 2,
    valinit=scalemean,
)
c_slider.on_changed(update_scale_value)

slider2_ax = plt.axes([0.1, 0.02, 0.8, 0.03])
mult_slider = Slider(
    slider2_ax,
    "Mesh density",
    1,
    30,
    valinit=10,
)
mult_slider.on_changed(update_mult_value)

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
scale_value = c_slider.val

mult_value = mult_slider.val
xx, yy = np.meshgrid(
    np.linspace(0, data.shape[1], int((data.shape[1] * int(mult_value)))),
    np.linspace(0, data.shape[0], int((data.shape[0] * int(mult_value)))),
    indexing="xy",
)


surf = ax.plot_surface(xx, yy, interp((xx, yy)), cmap=cm.plasma)
# ax.set_title("Interpolated Plot")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_box_aspect([data.shape[1], data.shape[0], scale_value])

for n in [ax]:
    n.set_xlim(0, data.shape[1])
    n.set_ylim(0, data.shape[0])
    n.set_zlim(np.amin(data, axis=None), np.amax(data, axis=None))


# Create Checkbuttons


radio_background = "lightgoldenrodyellow"
pax = plt.axes([0.05, 0.15, 0.12, 0.05])
radio = RadioButtons(
    pax,
    (
        "nearest",
        "linear",
    ),
    # "cubic", "quintic"),
)
radio.on_clicked(interp_method)

fig.colorbar(surf, ax=[ax], shrink=0.5, aspect=50, pad=0.1)
title_text = """
Table Flatness Probe Mesh Interpreter
Interpolated Plot:
"""
fig.text(0.5, 0.9, title_text, fontsize=34, ha="center")

info = f"""
X size: {data.shape[1]}
Y size: {data.shape[0]}
Z max : {np.max(data)}
Z min : {np.min(data)}
Z mean: {format(np.mean(data), ".4f")}


"""
fig.text(0.05, 0.5, info)


# Get the current figure manager
mng = plt.get_current_fig_manager()

# Maximize the window (works on Ubuntu as well)
mng.window.state("zoomed")

# Set the window title
mng.set_window_title("Table Flatness Probe Mesh Interpreter")
plt.show()

# Maximize the window
