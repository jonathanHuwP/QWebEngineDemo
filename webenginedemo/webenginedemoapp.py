## -*- coding: utf-8 -*-
"""
Created on Tue 17 Nov 2020

Adapted from Qt Documentation page
https://doc.qt.io/qt-5/qtwebengine-webenginewidgets-minimal-example.html

Available under GNU Free Documentation License version 1.3

This work was funded by Joanna Leng's EPSRC funded RSE Fellowship (EP/R025819/1)

@copyright 2020
@author: j.h.pickering@leeds.ac.uk and j.leng@leeds.ac.uk
"""
# set up linting conditions
# pylint: disable = too-few-public-methods
# pylint: disable = c-extension-no-member
# pylint: disable = import-error

import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc

from webenginedemo.gui.webenginedemomainwindow import WebEngineDemoMainWindow

class WebEngineDemoApp(qw.QApplication):
    """
    app for the demo
    """

    def __init__(self, args):
        super().__init__(args)
        self.setOrganizationName("QtExamples")
        self.setApplicationName("HtmlDemoApp")
        self.setApplicationVersion("B0.0")
        self.setAttribute(qc.Qt.AA_EnableHighDpiScaling)

        window = WebEngineDemoMainWindow()
        window.show()

        self.exec_()    # enter event loop
