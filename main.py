#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout
from widgets.params_widget import ParamsWidget

if __name__ == '__main__':

    # Init application
    app = QApplication(sys.argv)
    # Init widgets
    main_window = QMainWindow()
    layout = QHBoxLayout()
    params_widget = ParamsWidget()
    central_widget = QWidget()
    # Place widgets
    layout.addWidget(params_widget)
    central_widget.setLayout(layout)
    main_window.setCentralWidget(central_widget)
    # Show
    main_window.show()
    sys.exit(app.exec_())