from PyQt5 import QtWidgets
from ui_forms.settings import Ui_Form
import sys


class ParamsWidget(QtWidgets.QWidget):

    def __init__(self):
        super(ParamsWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)