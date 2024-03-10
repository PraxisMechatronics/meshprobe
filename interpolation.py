from scipy.interpolate import RegularGridInterpolator
import numpy as np
import matplotlib.pyplot as plt

x, y = np.array([-2, 0, 4]), np.array([-2, 0, 2, 5])


def ff(x, y):
    return x**2 + y**2


xg, yg = np.meshgrid(x, y, indexing="ij")

data = ff(xg, yg)
interp = RegularGridInterpolator((x, y), data, bounds_error=False, fill_value=None)

fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ax.scatter(xg.ravel(), yg.ravel(), data.ravel(), s=60, c="k", label="data")

xx = np.linspace(-4, 9, 31)
yy = np.linspace(-4, 9, 31)
X, Y = np.meshgrid(xx, yy, indexing="ij")

# interpolator
ax.plot_wireframe(
    X,
    Y,
    interp((X, Y)),
    rstride=3,
    cstride=3,
    alpha=0.4,
    color="m",
    label="linear interp",
)


# ground truth
ax.plot_wireframe(
    X,
    Y,
    ff(X, Y),
    rstride=3,
    cstride=3,
    alpha=0.4,
    label="ground truth",
)

plt.legend()
plt.show()
