import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QRect

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
import matplotlib.pyplot as plt
import random
import numpy as np

from ViewModel import PlotViewModel


class Plot(FigureCanvasQTAgg):
    def __init__(self, view_model: PlotViewModel, width, height, parent, layout, dpi=100):
        self.view_model = view_model

        fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        FigureCanvasQTAgg.__init__(self, fig)
        self.setParent(parent)
        navigation_toolbar = NavigationToolbar(self, parent)
        layout.addWidget(navigation_toolbar)
        self.axes = self.figure.subplots()

        self.view_model.load_data()

        self.dataY = self.view_model.fft.magnitudes
        self.dataX = self.view_model.fft.frequencies

        self.axes.plot(self.dataX, self.dataY, 'r-')
        self.axes.set_title(self.view_model.title)

        self.cursor = SnapToCursor(self.axes, self.dataX, self.dataY, self)
        self.figure.canvas.mpl_connect('motion_notify_event', self.cursor.mouse_move)
        self.axes.format_coord = lambda x, y: self.view_model.format_current_point_info(self.cursor.currentX, self.cursor.currentY)

        self.draw()



class SnapToCursor:
    def __init__(self, ax, x, y, plotCanvas):
        self.ax = ax
        self.plotCanvas = plotCanvas

        self.lx = ax.axhline(color='lightGray')  # the horiz line
        self.ly = ax.axvline(color='lightGray')  # the vert line
        self.x = x
        self.y = y

        self.currentX = x[0]
        self.currentY = y[0]

        # text location in axes coords
        # self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)

    def mouse_move(self, event):
        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata

        current_point_index = np.searchsorted(self.x, [x])[0]
        self.currentX = self.x[current_point_index]
        self.currentY = self.y[current_point_index]

        self.plotCanvas.draw()
        self.lx.set_ydata(self.currentY)
        self.ly.set_xdata(self.currentX)

        # self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        # print('x=%1.2f, y=%1.2f' % (x, y))


# class PlotCanvas(FigureCanvasQTAgg):
#     def __init__(self, width, height, parent=None, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         FigureCanvasQTAgg.__init__(self, fig)
#         self.setParent(parent)
#
#         self._main = QtWidgets.QWidget()
#         parent.setCentralWidget(self._main)
#         layout = QtWidgets.QVBoxLayout(self._main)
#         navigation_toolbar = NavigationToolbar(self, parent)
#
#         self.button = QPushButton('Plot')
#         self.button.setToolTip('This is a <b>QPushButton</b> widget')
#         self.button.clicked.connect(self.plot)
#         navigation_toolbar.addWidget(self.button)
#
#         # navigation_toolbar.addWidget(self.cb)
#
#         layout.addWidget(navigation_toolbar)
#         layout.addWidget(self)
#
#         FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
#         FigureCanvasQTAgg.updateGeometry(self)
#
#         self.axes = self.figure.subplots()
#
#         self.plot()
#
#     def plot(self):
#         self.data = [random.random() for i in range(25)]
#         self.axes.plot(self.data, 'r-')
#         self.axes.set_title('PyQt Matplotlib Example')
#
#         self.cursor = SnapToCursor(self.axes, [i for i in range(25)], self.data, self)
#         self.figure.canvas.mpl_connect('motion_notify_event', self.cursor.mouse_move)
#
#         self.axes.format_coord = lambda x, y: 'x={:01.2f}, y={:01.2f}'.format(self.cursor.currentX, self.cursor.currentY)
#
#         self.draw()