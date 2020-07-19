from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
import numpy as np
from math import cos, radians, pi
from timeit import default_timer as timer


def f(xy):
    x = xy[0]
    y = xy[1]
    if x > 45 and y > 45:
        return 2.0
    if 0 < x < 10:
        return -2.0
    if x < -45 and y < -45:
        return -1.0
    if x < 0 and y > 45:
        return 1.0
    return 0


class DnaCalc(QObject):

    @staticmethod
    def calculate(params):
        start = timer()
        print("start")
        n_x = params["grid_number_az"]
        n_y = params["grid_number_el"]
        # x = np.radians(np.linspace(-60, 60, n_x))
        # y = np.radians(np.linspace(-60, 60, n_y))
        x = np.linspace(-60, 60, n_x)
        y = np.linspace(-60, 60, n_y)
        yy, xx = np.meshgrid(y, x)
        xy = np.c_[xx.ravel(), yy.ravel()]
        dna = DnaCalc.create_dna(params)
        data = np.fromiter(map(dna, xy.tolist()), dtype=float).reshape(n_x, n_y)
        end = timer()
        print("gotovo", end - start, "seconds")
        return data

    # "beam_angle_az", "beam_angle_el", \
    # "mainline_width_az", "mainline_width_el", \
    # "grid_number_az", "grid_number_el", \
    # "linear", "log"
    # M.B. using numpy methods
    @staticmethod
    def create_dna(params):
        beam_angle_az = params["beam_angle_az"]
        beam_angle_el = params["beam_angle_el"]
        mainline_width_az = params["mainline_width_az"]
        mainline_width_el = params["mainline_width_el"]
        l_main = 3.0
        l_side = 1.0

        def l_(x, y):
            if abs(x - beam_angle_az) < mainline_width_az / cos(radians(beam_angle_az)) and \
                    abs(y - beam_angle_el) < mainline_width_el / cos(radians(beam_angle_el)):
                return l_main
            return l_side

        def dna_(xy):
            x = xy[0]
            y = xy[1]
            G_x = abs(cos(pi * (x - beam_angle_az * cos(radians(beam_angle_az)) / 2.0 / mainline_width_az)))
            G_y = abs(cos(pi * (y - beam_angle_el * cos(radians(beam_angle_el)) / 2.0 / mainline_width_el)))
            return G_x * G_y * l_(x, y)

        return dna_

    calculated = pyqtSignal()

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
        self.pool.apply_async(DnaCalc.calculate, (params.copy(),), callback=self.set_calculated, error_callback=print)
