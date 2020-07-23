#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout
from widgets.params_widget import ParamsWidget
from widgets.bp2d_widget import Bp2DWidget
from widgets.bp3d_widget import Bp3DWidget
from calculators.beam_pattern_calc import BeamPatternCalc


if __name__ == '__main__':

    # Init application
    app = QApplication(sys.argv)
    # Init widgets
    main_window = QMainWindow()
    layout = QHBoxLayout()
    params_widget = ParamsWidget()
    central_widget = QWidget()
    bp2DWidget = Bp2DWidget()
    bp3DWidget = Bp3DWidget()
    # Init calculators
    bpCalc = BeamPatternCalc(params_widget)
    # Set connections
    params_widget.paramsChanged.connect(bpCalc.start_calc)
    bpCalc.calculated.connect(bp2DWidget.on_data_changed)
    bpCalc.calculated.connect(bp3DWidget.on_data_changed)
    params_widget.on_params_changed()
    # Place widgets
    layout.addWidget(params_widget)
    layout.addWidget(bp2DWidget, 1)
    layout.addWidget(bp3DWidget, 1)
    central_widget.setLayout(layout)
    main_window.setCentralWidget(central_widget)
    # Show
    main_window.show()

    sys.exit(app.exec_())