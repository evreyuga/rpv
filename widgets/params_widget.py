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

    def params(self):
        return self.ui.beam_angle_az_cb.value(), self.ui.beam_angle_el_cb.value(), \
               self.ui.mainline_width_az_cb.value(), self.ui.mainline_width_el_cb.value(), \
               self.ui.grid_number_az_cb.value(), self.ui.grid_number_el_cb.value(), \
               self.ui.linear_rb.isChecked(), self.ui.log_rb.isChecked()

    def param_names(self):
        return "beam_angle_az", "beam_angle_el", \
               "mainline_width_az", "mainline_width_el", \
               "grid_number_az", "grid_number_el", \
               "linear", "log"

    def params_dict(self):
        return {k: v for k, v in zip(self.param_names(), self.params())}

    @pyqtSlot()
    def onParamsChanged(self):
        self.paramsChanged.emit(self.params_dict())

    def __set_connections(self):
        self.ui.beam_angle_az_cb.valueChanged.connect(self.onParamsChanged)
        self.ui.beam_angle_el_cb.valueChanged.connect(self.onParamsChanged)
        self.ui.mainline_width_az_cb.valueChanged.connect(self.onParamsChanged)
        self.ui.mainline_width_el_cb.valueChanged.connect(self.onParamsChanged)
        self.ui.grid_number_az_cb.valueChanged.connect(self.onParamsChanged)
        self.ui.grid_number_el_cb.valueChanged.connect(self.onParamsChanged)
        self.ui.linear_rb.toggled.connect(self.onParamsChanged)
        self.ui.log_rb.toggled.connect(self.onParamsChanged)




