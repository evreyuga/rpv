from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout
from PyQt5.QtCore import pyqtSlot
import numpy as np
import pyvista as pv
from pyqtgraph.graphicsItems.GradientEditorItem import Gradients
from pyvistaqt import QtInteractor
from pyqtgraph import ColorMap
from matplotlib.colors import ListedColormap


class Bp3DWidget(QWidget):

    def __init__(self):
        super(Bp3DWidget, self).__init__()
        self.frame = QFrame()
        layout = QVBoxLayout()
        colormap = ColorMap(*zip(*Gradients["bipolar"]["ticks"])).getLookupTable() / 255.0
        self.colormap = ListedColormap(colormap)
        self.plotter = QtInteractor(self.frame)
        layout.addWidget(self.plotter.interactor)
        self.frame.setLayout(layout)
        self.setLayout(layout)

    @pyqtSlot()
    def on_data_changed(self):
        sender = self.sender()
        grid = Bp3DWidget.__create_grid(sender.data)
        self.plotter.clear()
        self.plotter.add_mesh(grid, scalars=np.rot90(sender.data)[::-1], cmap=self.colormap)

    @staticmethod
    def __create_grid(data):
        shape = np.shape(data)
        # M.B. plot add to params
        az_grid = np.deg2rad(np.linspace(-60, 60, shape[1]))
        el_grid = np.deg2rad(np.linspace(-60, 60, shape[0]))
        az_mesh, el_mesh = np.meshgrid(az_grid, el_grid)
        r_mesh = data
        x_mesh = np.cos(az_mesh) * np.cos(el_mesh) * r_mesh
        y_mesh = np.sin(az_mesh) * np.cos(el_mesh) * r_mesh
        z_mesh = np.sin(el_mesh) * r_mesh
        grid = pv.StructuredGrid(x_mesh, y_mesh, z_mesh)
        return grid
