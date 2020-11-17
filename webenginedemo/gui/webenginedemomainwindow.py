## -*- coding: utf-8 -*-
"""
Created on Mon 16 Nov 2020

Adapted from Qt Documentation page
https://doc.qt.io/qt-5/qtwebengine-webenginewidgets-minimal-example.html

Available under GNU Free Documentation License version 1.3

This work was funded by Joanna Leng's EPSRC funded RSE Fellowship (EP/R025819/1)

@copyright 2020
@author: j.h.pickering@leeds.ac.uk and j.leng@leeds.ac.uk
"""
# set up linting conditions
# pylint: disable = too-many-public-methods
# pylint: disable = c-extension-no-member
# pylint: disable = import-error

import os
import pathlib

import PyQt5.QtWidgets as qw
import PyQt5.QtGui as qg
import PyQt5.QtCore as qc
import PyQt5.QtWebEngineWidgets as qe
import PyQt5.QtPrintSupport as qp

from webenginedemo.gui.Ui_webenginedemomainwindow import Ui_WebEngineDemoMainWindow

class WebEngineDemoMainWindow(qw.QMainWindow, Ui_WebEngineDemoMainWindow):
    """
    class providing a crude web viewer
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self._doc = qg.QTextDocument()
        self.make_document()

        view = qe.QWebEngineView()
        self._scrollArea.setWidget(view)

    def make_document(self):
        """
        make a string of HTML, to use in example

            Returns:
                a HTML string
        """

        path = pathlib.Path(os.getcwd()).joinpath("resources").joinpath("demo_figure.png")
        height = 512
        width = 512

        html = "<h1>The Tlite</h1>"
        html += "<h2>HTML Image</h2>"
        html += f"<img src=\"{path}\" width=\"{width}\" height=\"{height}\">"
        self._doc.setHtml(html)

    @qc.pyqtSlot()
    def load_web_page(self):
        """
        load a web page
        """
        reply = qw.QInputDialog.getText(self,
                                        "Project Name",
                                        "Proj Name",
                                        qw.QLineEdit.Normal,
                                        "https://www.bbc.co.uk/news")
        if not reply[1]:
            return

        self._scrollArea.widget().setUrl(qc.QUrl(reply[0]))

    @qc.pyqtSlot()
    def load_demo(self):
        """
        load the hard coded demonstration document
        """
        # a QUrl to local file is required to allow QWebEngine to access local files
        # the altrnativ is to pass "--disable-web-security" as an argument
        # to QCoreApplication on startup, which leavs the application at risk
        self._scrollArea.widget().setHtml(self._doc.toHtml(), qc.QUrl("file://"))

    @qc.pyqtSlot()
    def save_demo_html(self):
        """
        save the hard coded demonstration document as a html file
        """
        utf = 'utf-8'
        file_types = "Hypertext Markup Language (*.html);;All files (*.*)"
        file_path, _ = qw.QFileDialog.getSaveFileName(self,
                                                     "Save Demonstration As Html",
                                                     "document",
                                                     file_types)

        if file_path is None or file_path == '':
            return

        # construct a python byte array out of sting "utf-8" using "utf-8" as encoding
        encoding_py = bytearray(utf, utf)

        # construct a Qt byte array object from the python (you don't have to do this step)
        encoding = qc.QByteArray(encoding_py)

        with open(file_path, 'w') as out_file:
            out_file.write(self._doc.toHtml(encoding))

    @qc.pyqtSlot()
    def save_image(self):
        """
        callback for saving the web engine's contents as a png file
        """
        file_types = "Portable Network Graphics PNG (*.png);;All files (*.*)"
        file_path, _ = qw.QFileDialog.getSaveFileName(self,
                                                     "Save Page As Image",
                                                     "image.png",
                                                     file_types)

        if file_path is None or file_path == '':
            return

        pixmap = self._scrollArea.widget().grab()
        print(f"Pixmap {pixmap}, Path {file_path}")
        if pixmap is not None:
            pixmap.save(file_path)

    @qc.pyqtSlot()
    def save_html(self):
        """
        callback for saving the web engine's contents as a HTML file
        """
        file_types = "Hypertext Markup Language (*.html);;All files (*.*)"
        file_path, _ = qw.QFileDialog.getSaveFileName(self,
                                                     "Save Page As Html",
                                                     "websave",
                                                     file_types)

        if file_path is None or file_path == '':
            return

        # inner function that will carry out the printing
        def file_write(text):
            with open(file_path, 'w') as out_file:
                out_file.write(text)

        self._scrollArea.widget().page().toHtml(file_write)

    @qc.pyqtSlot()
    def save_view_pdf(self):
        """
        callback for saving the web engine's contents a PDF file
        """
        file_types = "PDF (*.pdf);;All files (*.*)"
        file_path, _ = qw.QFileDialog.getSaveFileName(self,
                                                     "Save Page As",
                                                     "myfile",
                                                     file_types)

        if file_path is None or file_path == '':
            return

        self._scrollArea.widget().page().printToPdf(file_path)

    @qc.pyqtSlot()
    def save_doc_pdf(self):
        """
        callback for saving the contents a PDF file, using a QPrinter
        """
        file_types = "PDF (*.pdf);;All files (*.*)"
        file_path, _ = qw.QFileDialog.getSaveFileName(self,
                                                     "Save Page As",
                                                     "myfile",
                                                     file_types)

        if file_path is None or file_path == '':
            return

        printer = qp.QPrinter(qp.QPrinter.PrinterResolution)
        printer.setOutputFormat(qp.QPrinter.PdfFormat)
        printer.setPaperSize(qp.QPrinter.A4)
        printer.setOutputFileName(file_path)

        self._doc.print(printer)
