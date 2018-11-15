import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QRect

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QComboBox, QAction, QSpinBox, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.cbook import Stack
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
import matplotlib.pyplot as plt
import random
import numpy as np

from ViewModel import PlotViewModel

import Controls

class Plot(FigureCanvasQTAgg):
    def __init__(self, view_model: PlotViewModel, width, height, parent, layout, dpi=100):
        self.view_model = view_model

        fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        FigureCanvasQTAgg.__init__(self, fig)
        self.setParent(parent)
        self.navigation_toolbar = NavigationToolbar2QT(self, self)
        layout.addWidget(self.navigation_toolbar)

        filter_spin_label = QLabel(self.view_model.filter_spin_label_text, self)
        self.navigation_toolbar.addWidget(filter_spin_label)

        filter_spin = QSpinBox(self)
        filter_spin.valueChanged.connect(self._filter_spin_value_changed)
        self.navigation_toolbar.addWidget(filter_spin)

        close_button = QPushButton(self.view_model.close_button_text) #QAction(QIcon(self.view_model.close_button_icon_path), self.view_model.close_button_text, self)
        # close_button.setShortcut('Ctrl+Shift+Q')
        #close_button.setStatusTip()
        close_button.clicked.connect(self._close_button_click)
        self.navigation_toolbar.addWidget(close_button)

        subtract_comobobox = Controls.Che

        self.axes = self.figure.subplots()
        self.axes.format_coord = lambda x, y: ""
        self.view_model.load_data()

        self._show_plot()

        #FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        #FigureCanvasQTAgg.updateGeometry(self)

    def _show_plot(self):
        result = self.view_model.get_result()
        self.dataY = result.magnitudes
        self.dataX = result.frequencies

        if len(self.dataX) == 0 or len(self.dataY) == 0:
            return

        self.axes.clear()

        self.axes.plot(self.dataX, self.dataY, drawstyle='steps-mid', zorder=1, lw=1, color='#d4d4d4') # 'r-' 'bo'
        self.axes.scatter(self.dataX, self.dataY, s=5, zorder=2)
        #self.axes.magnitude_spectrum(self.dataY, self.dataX[0])

        self.axes.grid(color='#ececec')
        #self.axes.set_title(self.view_model.title)
        self.axes.text(0, 1, self.view_model.title, transform=self.axes.transAxes)

        format_coord_lambda = lambda x, y: self.view_model.format_current_point_info(self.cursor.currentX, self.cursor.currentY)

        self.cursor = SnapToCursor(self.axes, self.dataX, self.dataY, self, format_coord_lambda)

        self.figure.canvas.mpl_connect('motion_notify_event', self.cursor.mouse_move)
        self.figure.canvas.mpl_connect('scroll_event', self._scroll_event)

        self.draw()

    def _filter_spin_value_changed(self, new_value: int):
        self.view_model.set_filter(abs(new_value))
        self._show_plot()
        self.navigation_toolbar.forward()

    def _close_button_click(self):
        self.setParent(None)
        self.navigation_toolbar.setParent(None)

    def _scroll_event(self, event):
        print(event)


class SnapToCursor:
    def __init__(self, ax, x, y, plot_canvas, format_coord_lambda):
        self.ax = ax
        self.plot_canvas = plot_canvas

        self.lx = ax.axhline(color='lightGray')  # the horiz line
        self.ly = ax.axvline(color='lightGray')  # the vert line
        self.x = x
        self.y = y

        self.currentX = x[0]
        self.currentY = y[0]

        self.format_coord_lambda = format_coord_lambda

        # text location in axes coords
        self.txt = ax.text(0.5, 0.99, '', fontsize=8, horizontalalignment='center', verticalalignment='top', transform=ax.transAxes)

    def mouse_move(self, event):
        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata

        current_point_index = np.searchsorted(self.x, [x])[0]

        self.currentX = self.x[current_point_index] if current_point_index < len(self.x) else self.x[len(self.x) - 1]
        self.currentY = self.y[current_point_index] if current_point_index < len(self.y) else self.y[len(self.y) - 1]

        self.plot_canvas.draw()
        self.lx.set_ydata(self.currentY)
        self.ly.set_xdata(self.currentX)

        self.txt.set_text(self.format_coord_lambda(x, y))
