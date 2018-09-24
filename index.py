import sys
import datetime

from PyQt5.QtCore import QSize, QRect, QDate, QDateTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QComboBox, QGroupBox, QCalendarWidget, QDateTimeEdit, QLabel
from PyQt5.QtGui import QIcon

from matplotlib.backends.qt_compat import QtCore, QtWidgets

import PlotCanvas
from ViewModel import AppViewModel
from Repository.MsAccessRepository import MsAccessRepository
from Service.DataService import DataService


class App(QMainWindow):
    def __init__(self, argv):
        super(App, self).__init__()
        db_file_full_path =  './Resources/data/db_обнуленная.mdb' if len(argv) < 2 else argv[1]
        ms_access_repo = MsAccessRepository(MsAccessRepository.create_connect_string(db_file_full_path))
        self.view_model = AppViewModel(DataService(ms_access_repo), dev_mode=len(argv) < 2)

        self._init_ui()

        self.plots = []
        self.show()

    def _init_ui(self):
        left = 30; top = 60; width = 640; height = 400

        self.setWindowTitle(self.view_model.title)
        self.setGeometry(left, top, width, height)

        self._create_toolbar()
        self._create_main_layout()

    def _create_toolbar(self):
        self.main_toolbar = self.addToolBar('MainToolbar')

        self.curve_combobox_label = QLabel(self.view_model.curve_combobox_label_text, self)
        self.main_toolbar.addWidget(self.curve_combobox_label)

        self.curve_combobox = QComboBox(self)
        #self.curve_combobox.setGeometry(QRect(40, 40, 491, 31))
        #self.curve_combobox.setObjectName("CurveCombobox")
        [self.curve_combobox.addItem(str_val, item) for str_val, item in self.view_model.get_line_names()]
        self.curve_combobox.setCurrentIndex(self.view_model.current_line.value)
        self.curve_combobox.currentIndexChanged.connect(self._curve_combobox_selection_change)
        self.main_toolbar.addWidget(self.curve_combobox)

        self.date_from_widget = self._create_date_time_picker(self.view_model.date_from) #QDate.currentDate().addDays(-1)
        self.date_from_widget.dateTimeChanged.connect(self._date_from_changed)

        self.main_toolbar.addWidget(self.date_from_widget)

        self.date_to_widget = self._create_date_time_picker(self.view_model.date_to) #QDateTime.currentDateTime()
        self.date_to_widget.dateTimeChanged.connect(self._date_to_changed)
        self.main_toolbar.addWidget(self.date_to_widget)

        self.add_plot_button = QPushButton(self.view_model.add_button_text)
        self.add_plot_button.setToolTip(self.view_model.add_button_tooltip)
        self.add_plot_button.clicked.connect(self._add_plot_button_clicked)
        self.main_toolbar.addWidget(self.add_plot_button)

    def _create_date_time_picker(self, initial_date: QDateTime):
        result = QDateTimeEdit(initial_date, self)
        result.setDisplayFormat(self.view_model.date_time_pickers_format)
        result.setCalendarPopup(True)

        return result

    def _create_main_layout(self):
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        self.main_layout = QtWidgets.QVBoxLayout(self._main)
        self.setLayout(self.main_layout)

    def _add_plot_button_clicked(self):
        new_plot = PlotCanvas.Plot(self.view_model.create_plot_view_model(), width=5, height=4, parent=self, layout=self.main_layout)
        self.plots.append(new_plot)
        self.main_layout.addWidget(new_plot)

    def _curve_combobox_selection_change(self, i):
        self.view_model.set_current_line(self.curve_combobox.currentData())

    def _date_from_changed(self, current_time: QDateTime):
        self.view_model.set_current_dates_from_to(current_time.toPyDateTime())

    def _date_to_changed(self, current_time: QDateTime):
        self.view_model.set_current_dates_from_to(current_time.toPyDateTime(), True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App(sys.argv)
    sys.exit(app.exec_())
