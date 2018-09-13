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


class SnaptoCursor:
    """
    Like Cursor but the crosshair snaps to the nearest x,y point
    For simplicity, I'm assuming x is sorted
    """

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

        indx = np.searchsorted(self.x, [x])[0]
        self.currentX = self.x[indx]
        self.currentY = self.y[indx]
        # update the line positions

        self.plotCanvas.draw()
        self.lx.set_ydata(self.currentY)
        self.ly.set_xdata(self.currentX)

        # self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        # print('x=%1.2f, y=%1.2f' % (x, y))


class PlotCanvas(FigureCanvasQTAgg):
    def __init__(self, width, height, parent=None, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvasQTAgg.__init__(self, fig)
        self.setParent(parent)

        self._main = QtWidgets.QWidget()
        parent.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)
        navigation_toolbar = NavigationToolbar(self, parent)

        self.button = QPushButton('Plot')
        self.button.setToolTip('This is a <b>QPushButton</b> widget')
        self.button.clicked.connect(self.plot)
        navigation_toolbar.addWidget(self.button)

        self.cb = QComboBox()
        self.cb.setGeometry(QRect(40, 40, 491, 31))
        self.cb.setObjectName(("comboBox"))
        self.cb.addItem("PyQt")
        self.cb.addItem("Qt")
        self.cb.addItem("Python")
        self.cb.addItem("Example")
        self.cb.currentIndexChanged.connect(self.selectionchange)

        navigation_toolbar.addWidget(self.cb)

        layout.addWidget(navigation_toolbar)
        layout.addWidget(self)

        FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

        self.axes = self.figure.subplots()

        self.plot()

    def selectionchange(self, i):
        print("Items in the list are :")

        for count in range(self.cb.count()):
            print(self.cb.itemText(count))

        print("Current index", i, "selection changed ", self.cb.currentText())

    def plot(self):
        self.data = [random.random() for i in range(25)]
        self.axes.plot(self.data, 'r-')
        self.axes.set_title('PyQt Matplotlib Example')

        self.cursor = SnaptoCursor(self.axes, [i for i in range(25)], self.data, self)
        self.figure.canvas.mpl_connect('motion_notify_event', self.cursor.mouse_move)

        self.axes.format_coord = lambda x, y: 'x={:01.2f}, y={:01.2f}'.format(self.cursor.currentX, self.cursor.currentY)

        self.draw()
