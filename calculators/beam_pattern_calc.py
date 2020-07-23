from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from multiprocessing import Pool
import numpy as np
from math import radians
from timeit import default_timer as timer


class BeamPatternCalc(QObject):

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
        print("Calculating start")
        start = timer()
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
        steering_angle_az = np.full(shape, radians(params["steering_angle_az"]), dtype=float)
        steering_angle_el = np.full(shape, radians(params["steering_angle_el"]), dtype=float)
        main_lobe_width_az = np.full(shape, radians(params["main_lobe_width_az"]), dtype=float)
        main_lobe_width_el = np.full(shape, radians(params["main_lobe_width_el"]), dtype=float)
        # Beam Pattern Expression {
        l = (np.abs(az - steering_angle_az) < main_lobe_width_az / np.cos(steering_angle_az)) & \
            (np.abs(el - steering_angle_el) < main_lobe_width_el / np.cos(steering_angle_el))
        l = np.array(l, dtype=int) * (l_max - 1) + 1
        G_az = np.abs(np.cos(np.pi * (az - steering_angle_az) * np.cos(steering_angle_az) / 2.0 / main_lobe_width_az))
        G_el = np.abs(np.cos(np.pi * (el - steering_angle_el) * np.cos(steering_angle_el) / 2.0 / main_lobe_width_el))
        data = G_az * G_el * l
        # }
        end = timer()
        print("Calculating took", end - start, "seconds")
        return data

    calculated = pyqtSignal()

    def __init__(self, *args):
        super(BeamPatternCalc, self).__init__(*args)
        self.pool = Pool(1)
        self.data = None

    def set_calculated(self, data):
        self.data = data
        self.calculated.emit()

    @pyqtSlot(dict)
    def start_calc(self, params):
        self.pool.terminate()
        self.pool = Pool(1)
        self.pool.apply_async(BeamPatternCalc.calculate, (params.copy(),), callback=self.set_calculated)
