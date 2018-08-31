import pandas as ps
from tkinter import Tk, Label, Button
import numpy as np
import matplotlib.pyplot as plt

import fftlib

# class MyFirstGUI:
#     def __init__(self, master):
#         self.master = master
#         master.title("A simple GUI")
#
#         self.label = Label(master, text="This is our first GUI!")
#         self.label.pack()
#
#         self.greet_button = Button(master, text="Greet", command=self.greet)
#         self.greet_button.pack()
#
#         self.close_button = Button(master, text="Close", command=master.quit)
#         self.close_button.pack()
#
#     def greet():
#         print("Greetings!")

# root = Tk()
# my_gui = MyFirstGUI(root)
# root.mainloop()

# ps = ps.read_excel('Мощность.xls', sheet_name="POVER")
# data = ps['К408А'].values
# N = data.size
# measureTime = 3.0
#
# t = np.linspace(0, measureTime * N, N)
#
# plt.figure()
# plt.plot(t, data)
# plt.xlim(0, N)
# plt.show()

import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QToolTip, QMessageBox, QWidget, \
    QDesktopWidget, QMainWindow
from PyQt5.QtGui import QIcon, QFont

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import random


class Window(QMainWindow): # QDialog QWidget QMainWindow
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.setWindowTitle('Icon')
        self.setGeometry(300, 300, 300, 220)
        self.setWindowIcon(QIcon('web.png'))
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')
        self.center()
        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.addToolBar(self.toolbar)

        self.statusBar().showMessage('Ready')

        # Just some button connected to `plot` method
        self.button = QPushButton('Plot')
        self.button.setToolTip('This is a <b>QPushButton</b> widget')

        self.button.clicked.connect(self.plot)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def plot(self):
        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(10)]

        # instead of ax.hold(False)
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        # ax.hold(False) # deprecated, see above

        # plot data
        ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
