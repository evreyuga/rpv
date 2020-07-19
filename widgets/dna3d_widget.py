from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout
from PyQt5.QtCore import pyqtSlot

import numpy as np
from scipy.interpolate import interp2d

import pyvista as pv
from pyvistaqt import QtInteractor

def _cell_bounds(points, bound_position=0.5):
    """
    Calculate coordinate cell boundaries.

    Parameters
    ----------
    points: numpy.array
        One-dimensional array of uniformy spaced values of shape (M,)
    bound_position: bool, optional
        The desired position of the bounds relative to the position
        of the points.

    Returns
    -------
    bounds: numpy.array
        Array of shape (M+1,)

    Examples
    --------
    >>> a = np.arange(-1, 2.5, 0.5)
    >>> a
    array([-1. , -0.5,  0. ,  0.5,  1. ,  1.5,  2. ])
    >>> cell_bounds(a)
    array([-1.25, -0.75, -0.25,  0.25,  0.75,  1.25,  1.75,  2.25])
    """
    assert points.ndim == 1, "Only 1D points are allowed"
    diffs = np.diff(points)
    delta = diffs[0] * bound_position
    bounds = np.concatenate([[points[0] - delta], points + delta])
    return bounds

class Interpolator(object):

    def __init__(self, data):
        shape = np.shape(data)
        x_ = np.linspace(-60, 60, shape[1])
        y_ = np.linspace(-60, 60, shape[0])
        y_polar_ = 90 - y_
        self.interpolate_ = interp2d(x_, y_, data)

        # Approximate radius of the Earth
        RADIUS = 1

        # Longitudes and latitudes
        x = np.linspace(-60, 60, 20)
        y = np.linspace(-60, 60, 20)
        y_polar = 90.0 - y  # grid_from_sph_coords() expects polar angle

        xx, yy = np.meshgrid(x, y)

        # x- and y-components of the wind vector
        u_vec = np.cos(np.radians(xx))  # zonal
        v_vec = np.sin(np.radians(yy))  # meridional

        # Scalar data
        #scalar = u_vec ** 2 + v_vec ** 2
        scalar = self.interpolate_(x, y)

        # Create arrays of grid cell boundaries, which have shape of (x.shape[0] + 1)
        xx_bounds = _cell_bounds(x)
        yy_bounds = _cell_bounds(y_polar)
        # Vertical levels
        # in this case a single level slightly above the surface of a sphere
        # Number of vertical levels
        nlev = 10
        levels = [RADIUS * 1.01]

        # Dummy 3D scalar data
        scalar_3d = (
                scalar.repeat(nlev).reshape((*scalar.shape, nlev)) * np.arange(nlev)[np.newaxis, np.newaxis, :]
        ).transpose(2, 0, 1)
        z_scale = 10
        z_offset = RADIUS * 1.1

        # Now it's not a single level but an array of levels
        levels = z_scale * (np.linspace(0, 10, scalar_3d.shape[0] + 1)) ** 2 + z_offset

        # Create a structured grid by transforming coordinates
        grid_scalar_3d = pv.grid_from_sph_coords(xx_bounds, yy_bounds, levels)

        # Add data to the grid
        grid_scalar_3d.cell_arrays["example"] = np.array(scalar_3d).swapaxes(-2, -1).ravel("C")
        #grid_scalar_3d.cell_arrays["example"] = np.array(scalar).swapaxes(-2, -1).ravel("C")

        # Create a set of isosurfaces
        self.grid = grid_scalar_3d.cell_data_to_point_data().contour()#(isosurfaces=[1, 9])

    def __call__(self, x, y):
        return self.interpolate_(x, y)[0]


class Dna3DWidget(QWidget):

    def __init__(self):
        super(Dna3DWidget, self).__init__()
        self.frame = QFrame()
        layout = QVBoxLayout()
        self.plotter = QtInteractor(self.frame)
        layout.addWidget(self.plotter.interactor)
        self.frame.setLayout(layout)
        self.setLayout(layout)
        self.add_sphere()

    def add_sphere(self):
        sphere = pv.Sphere()
        self.plotter.add_mesh(sphere)
        self.plotter.reset_camera()

    @pyqtSlot()
    def onDataChaged(self):
        sender = self.sender()
        interpolator = Interpolator(sender.data)
        self.plotter.clear()
        self.plotter.add_mesh(interpolator.grid)