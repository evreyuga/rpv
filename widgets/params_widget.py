from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from ui_forms.settings import Ui_Form


class ParamsWidget(QtWidgets.QWidget):

    paramsChanged = pyqtSignal(dict)

    def __init__(self):
        super(ParamsWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.__set_connections()
        self.param_names = ("steering_angle_az", "steering_angle_el",
                            "main_lobe_width_az", "main_lobe_width_el",
                            "grid_number_az", "grid_number_el",
                            "linear", "log")

    def params(self):
        return self.ui.steering_angle_az_cb.value(), self.ui.steering_angle_el_cb.value(), \
               self.ui.main_lobe_width_az_cb.value(), self.ui.main_lobe_width_el_cb.value(), \
               self.ui.grid_number_az_cb.value(), self.ui.grid_number_el_cb.value(), \
               self.ui.linear_rb.isChecked(), self.ui.log_rb.isChecked()

    def names(self):
        return self.param_names

    def params_dict(self):
        return {k: v for k, v in zip(self.names(), self.params())}

    @pyqtSlot()
    def on_params_changed(self):
        self.paramsChanged.emit(self.params_dict())

    def __set_connections(self):
        self.ui.steering_angle_az_cb.valueChanged.connect(self.on_params_changed)
        self.ui.steering_angle_el_cb.valueChanged.connect(self.on_params_changed)
        self.ui.main_lobe_width_az_cb.valueChanged.connect(self.on_params_changed)
        self.ui.main_lobe_width_el_cb.valueChanged.connect(self.on_params_changed)
        self.ui.grid_number_az_cb.valueChanged.connect(self.on_params_changed)
        self.ui.grid_number_el_cb.valueChanged.connect(self.on_params_changed)
        self.ui.linear_rb.toggled.connect(self.on_params_changed)
        self.ui.log_rb.toggled.connect(self.on_params_changed)




