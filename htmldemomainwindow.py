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

import sys

import PyQt5.QtWidgets as qw
import PyQt5.QtGui as qg
import PyQt5.QtCore as qc
import PyQt5.QtWebEngineWidgets as qe
import PyQt5.QtPrintSupport as qp

from Ui_htmldemomainwindow import Ui_HtmlDemoMainWindow

class HtmlDemoMainWindow(qw.QMainWindow, Ui_HtmlDemoMainWindow):
    """
    class providing a crude web viewer
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self._doc = qg.QTextDocument()
        self.make_document()

        view = qe.QWebEngineView()
        #url = qc.QUrl("https://www.bbc.co.uk/news")
        #view.setUrl(url)
        view.setHtml(self._doc.toHtml())
        self._scrollArea.setWidget(view)

    def make_document(self):
        """
        make a string of HTML, to use in example

            Returns:
                a HTML string
        """
        html_string = "<h1>The Title</h1>"
        self._doc.setHtml(html_string)

    def save_image(self):
        """
        callback for saving the contents a png file
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

    def save_html(self):
        """
        callback for saving the contents a HTML file
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

    def save_view_pdf(self):
        """
        callback for saving the contents a PDF file, using the web engine itself
        """
        file_types = "PDF (*.pdf);;All files (*.*)"
        file_path, _ = qw.QFileDialog.getSaveFileName(self,
                                                     "Save Page As",
                                                     "myfile",
                                                     file_types)

        if file_path is None or file_path == '':
            return

        self._scrollArea.widget().page().printToPdf(file_path)

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

class HtmlDemoApp(qw.QApplication):
    """
    app for the demo
    """

    def __init__(self, args):
        super().__init__(args)
        self.setOrganizationName("QtExamples")
        self.setApplicationName("HtmlDemoApp")
        self.setApplicationVersion("B0.0")
        self.setAttribute(qc.Qt.AA_EnableHighDpiScaling)

        window = HtmlDemoMainWindow()
        window.show()

        self.exec_()    # enter event loop

if __name__ == "__main__":
    application = HtmlDemoApp(sys.argv)
