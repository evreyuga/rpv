#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout

from widgets.params_widget import ParamsWidget
from widgets.dna2d_widget import Dna2DWidget
from widgets.dna3d_widget import Dna3DWidget
from calculators.dna_calc import DnaCalc


if __name__ == '__main__':

    # Init application
    app = QApplication(sys.argv)
    # Init widgets
    main_window = QMainWindow()
    layout = QHBoxLayout()
    params_widget = ParamsWidget()
    central_widget = QWidget()
    dna2DWidget = Dna2DWidget()
    dna3DWidget = Dna3DWidget()
    # Init calculators
    dnaCalc = DnaCalc(params_widget)
    # Set connections
    params_widget.paramsChanged.connect(dnaCalc.start_calc)
    dnaCalc.calculated.connect(dna2DWidget.onDataChaged)
    dnaCalc.calculated.connect(dna3DWidget.onDataChaged)
    params_widget.onParamsChanged()
    # Place widgets
    layout.addWidget(params_widget)
    layout.addWidget(dna2DWidget, 1)
    layout.addWidget(dna3DWidget, 1)
    central_widget.setLayout(layout)
    main_window.setCentralWidget(central_widget)
    # Show
    main_window.show()

    sys.exit(app.exec_())