import sys
import datetime

from PyQt5.QtCore import QSize, QRect
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QComboBox, QGroupBox
from PyQt5.QtGui import QIcon

from matplotlib.backends.qt_compat import QtCore, QtWidgets

import PlotCanvas
from ViewModel import ViewModel
from Repository.MsAccessRepository import MsAccessRepository
from Service.DataService import DataService


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()

        self.init_ui()

        self.plots = []
        self.show()

    def init_ui(self):
        left = 30; top = 60; width = 640; height = 400

        self.setWindowTitle('Анализ спектров потребления транспортных линий')
        self.setGeometry(left, top, width, height)

        self.create_toolbar()
        self.create_main_layout()
        self.view_model = ViewModel(DataService(MsAccessRepository()))

    def create_toolbar(self):
        self.mainToolbar = self.addToolBar('MainToolbar')

        self.curveCombobox = QComboBox()
        self.curveCombobox.setGeometry(QRect(40, 40, 491, 31))
        self.curveCombobox.setObjectName("CurveCombobox")
        self.curveCombobox.addItem("PyQt")
        self.curveCombobox.addItem("Qt")
        self.curveCombobox.addItem("Python")
        self.curveCombobox.addItem("Example")
        self.curveCombobox.currentIndexChanged.connect(self.curve_combobox_selection_change)
        self.mainToolbar.addWidget(self.curveCombobox)

        self.addPlotButton = QPushButton('AddPlotButton')
        self.addPlotButton.setToolTip('Добавить <b>выбранный</b> график для анализа')
        self.addPlotButton.clicked.connect(self.add_plot_button_clicked)
        self.mainToolbar.addWidget(self.addPlotButton)

    def create_main_layout(self):
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        self.main_layout = QtWidgets.QVBoxLayout(self._main)
        self.setLayout(self.main_layout)

    def add_plot_button_clicked(self):
        new_plot = PlotCanvas.Plot(self.view_model, width=5, height=4, parent=self, layout=self.main_layout)
        self.plots.append(new_plot)
        self.main_layout.addWidget(new_plot)

    def curve_combobox_selection_change(self, i):
        print("Items in the list are :")

        for count in range(self.curveCombobox.count()):
            print(self.curveCombobox.itemText(count))

        print("Current index", i, "selection changed ", self.curveCombobox.currentText())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

    # import pyodbc
    #
    # MDB = './Resources/data/db_обнуленная.mdb'
    # DRV = [x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')][0] #'{Microsoft Access Driver (*.mdb)}'
    # PWD = ''
    #
    # connect_string = 'DRIVER={};DBQ={}'.format(DRV, MDB)
    # print(connect_string)
    #
    # con = pyodbc.connect(connect_string)
    # cur = con.cursor()
    #
    # tables = list(cur.tables())
    # for b in tables: print (b[2])
    #
    # cur = con.cursor()
    #
    # # run a query and get the results
    # SQL = 'SELECT MAX(ДатаИВремя) FROM Мощность;'  # your query goes here
    # rows = cur.execute(SQL).fetchall()
    # cur.close()
    #
    # print(rows[0][0])
    #
    # cur = con.cursor()
    # # run a query and get the results
    # SQL = "SELECT TOP 2 * FROM Мощность WHERE ДатаИВремя = ? ORDER BY ДатаИВремя DESC;"
    # params = (datetime.datetime(2018, 2, 25, 15, 52, 27))
    # #params = (datetime.datetime('2018-02-25 15:52:27'))
    # rows = cur.execute(SQL, params).fetchall()
    # cur.close()
    #
    # print(rows)
    #
    # columns = ['К408А', 'К408Б', 'К409А', 'К409Б', 'К427_1А', 'К427_1Б', 'К427_2А', 'К427_2Б', 'К502_1', 'К502_2']
    #
    # cur = con.cursor()
    # # run a query and get the results
    # SQL = "SELECT TOP 2 К408А FROM Мощность WHERE ДатаИВремя = ? ORDER BY ДатаИВремя DESC;"
    # params = (datetime.datetime(2018, 2, 25, 15, 52, 27))
    # # params = (datetime.datetime('2018-02-25 15:52:27'))
    # rows = cur.execute(SQL, params).fetchall()
    # cur.close()
    #
    # print(rows)
    #
    # con.close()