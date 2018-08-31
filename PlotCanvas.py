from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
import matplotlib.pyplot as plt
import random


class PlotCanvas(FigureCanvasQTAgg):
    def __init__(self, width, height, parent=None, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvasQTAgg.__init__(self, fig)
        self.setParent(parent)

        self._main = QtWidgets.QWidget()
        parent.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)
        layout.addWidget(NavigationToolbar(self, parent))
        layout.addWidget(self)

        FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)


        self.axes = self.figure.subplots() #fig.add_subplot(111)



        self.plot()

    def plot(self):
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('PyQt Matplotlib Example')
        self.draw()
