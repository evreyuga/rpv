from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from multiprocessing import Pool
import numpy as np


def f(xy):
    x = xy[0]
    y = xy[1]
    if x > 45 and y > 45:
        return 2.0
    if x < -45 and y < -45:
        return -1.0
    if x < -0 and y > 45:
        return 1.0
    return 0


class DnaCalc(QObject):

    calculated = pyqtSignal()

    @staticmethod
    def calculate(params):
        n_x = params["grid_number_az"]
        n_y = params["grid_number_el"]
        x = np.linspace(-60, 60, n_x)
        y = np.linspace(-60, 60, n_y)
        yy, xx = np.meshgrid(y, x)
        xy = np.c_[xx.ravel(), yy.ravel()]
        data = np.array(list(map(f, xy))).reshape(n_x, n_y)
        return data

    def __init__(self, *args):
        super(DnaCalc, self).__init__(*args)
        self.pool = Pool(1)
        self.data = None

    def set_calculated(self, data):
        self.data = data
        self.calculated.emit()

    @pyqtSlot(dict)
    def start_calc(self, params):
        self.pool.terminate()
        self.pool = Pool(1)
        self.pool.apply_async(DnaCalc.calculate, (params.copy(),), callback=self.set_calculated)
