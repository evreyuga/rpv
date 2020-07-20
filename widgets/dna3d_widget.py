from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout
from PyQt5.QtCore import pyqtSlot

import numpy as np

import pyvista as pv
from pyvistaqt import QtInteractor


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
        grid = Dna3DWidget.__create_grid(sender.data)
        self.plotter.clear()
        self.plotter.add_mesh(grid)

    @staticmethod
    def __create_grid(data):
        shape = np.shape(data)
        az_grid = np.deg2rad(np.linspace(-60, 60, shape[1]))
        el_grid = np.deg2rad(np.linspace(-60, 60, shape[0]))
        az_mesh, el_mesh = np.meshgrid(az_grid, el_grid)
        r_mesh = data
        x_mesh = np.cos(az_mesh) * np.cos(el_mesh) * r_mesh
        y_mesh = np.sin(az_mesh) * np.cos(el_mesh) * r_mesh
        z_mesh = np.sin(el_mesh) * r_mesh
        return pv.StructuredGrid(x_mesh, y_mesh, z_mesh)
