from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
import numpy as np
from math import radians


class DnaCalc(QObject):

    @staticmethod
    def calculate(params):
        n_x = params["grid_number_az"]
        n_y = params["grid_number_el"]
        logarithmic = params["log"]
        # M.B. to Gui params {
        l_max = 3.0
        x_range, y_range = 60, 60
        # }
        x_min, x_max = -x_range, x_range
        y_min, y_max = -y_range, y_range
        x = None
        y = None
        if logarithmic:
            x_log_space = np.logspace(-1, np.log10(x_range), n_x // 2)
            y_log_space = np.logspace(-1, np.log10(y_range), n_y // 2)
            x = np.hstack([-x_log_space[::-1], 0, x_log_space])
            y = np.hstack([-y_log_space[::-1], 0, y_log_space])
        else:
            x = np.linspace(x_min, x_max, n_x)
            y = np.linspace(y_min, y_max, n_y)
        az, el = np.meshgrid(np.deg2rad(x), np.deg2rad(y))
        shape = np.shape(az)
        beam_angle_az = np.full(shape, radians(params["beam_angle_az"]), dtype=float)
        beam_angle_el = np.full(shape, radians(params["beam_angle_el"]), dtype=float)
        mainline_width_az = np.full(shape, radians(params["mainline_width_az"]), dtype=float)
        mainline_width_el = np.full(shape, radians(params["mainline_width_el"]), dtype=float)
        l = (np.abs(az - beam_angle_az) < mainline_width_az / np.cos(beam_angle_az)) & \
            (np.abs(el - beam_angle_el) < mainline_width_el / np.cos(beam_angle_el))
        l = np.array(l, dtype=int) * (l_max - 1) + 1
        G_az = np.abs(np.cos(np.pi * (az - beam_angle_az) * np.cos(beam_angle_az) / 2.0 / mainline_width_az))
        G_el = np.abs(np.cos(np.pi * (el - beam_angle_el) * np.cos(beam_angle_el) / 2.0 / mainline_width_el))
        data = G_az * G_el * l
        return data

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
        self.pool.apply_async(DnaCalc.calculate, (params.copy(),), callback=self.set_calculated)
