from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QComboBox, QMainWindow, QApplication, QWidget, QVBoxLayout, QToolButton, \
    QMenu, QAction, QLineEdit, QListWidgetItem
from typing import List

import sys, os


class CheckableComboBox(QComboBox):

    class ItemModel:
        Title: str
        Checked: bool
        Index: int

        def __init__(self, title: str, index: int):
            self.Title = title
            self.Index = index
            self.Checked = False

    _items: List[ItemModel]

    def __init__(self, items: List[str]):
        super(CheckableComboBox, self).__init__()
        self.view().pressed.connect(self._item_pressed)
        self.setModel(QtGui.QStandardItemModel(self))
        self.setEditable(True)
        self.editTextChanged.connect(self._edit_text_changed)
        self._items = []
        current_item: int = 0
        for title in items:
            item_model: CheckableComboBox.ItemModel = CheckableComboBox.ItemModel(title, current_item)
            self._items.append(item_model)
            self.addItem(title, item_model)
            item = self.model().item(current_item, 0)
            item.setCheckState(QtCore.Qt.Unchecked)
            current_item += 1

    def _edit_text_changed(self, e):
        self.setEditText("sdsd,sdsd,sdsd")

    def _item_pressed(self, index: QtCore.QModelIndex):
        item: QtGui.QStandardItem = self.model().itemFromIndex(index)
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)

        model: QtGui.QStandardItemModel = index.model()

        print(self._items)
        print(model)
        #QtGui.QStandardItem
        #QListWidgetItem

        #self.setCurrentText("rrrr r r r r  r, rr")
        #self.setItemText(index, self.text)
        #self.lineEdit().displayText("dfdfdfdfdfdf")
        #self.setEditText("sdsd,sdsd,sdsd")

        #item.text = "dfdfdf"

class Dialog_01(QMainWindow):
    def __init__(self):
        super(QMainWindow,self).__init__()
        myQWidget = QWidget()
        myBoxLayout = QVBoxLayout()
        myQWidget.setLayout(myBoxLayout)
        self.setCentralWidget(myQWidget)
        self.ComboBox = CheckableComboBox(["sdds","eeq","sde"])
        # for i in range(3):
        #     self.ComboBox.addItem("Combobox Item " + str(i))
        #     item = self.ComboBox.model().item(i, 0)
        #     item.setCheckState(QtCore.Qt.Unchecked)


        myBoxLayout.addWidget(self.ComboBox)

        self.tool_button = QToolButton(self)
        self.tool_button.setText('Select Categories ')
        self.tool_menu = QMenu(self)
        for i in range(3):
            action = self.tool_menu.addAction("Category " + str(i))
            action.setCheckable(True)
            action.triggered.connect(self.item_pressed)

        self.tool_button.setMenu(self.tool_menu)
        self.tool_button.setPopupMode(QToolButton.InstantPopup)

        myBoxLayout.addWidget(self.tool_button)

    def item_pressed(self, e):
        print(self, e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog_1 = Dialog_01()
    dialog_1.show()
    dialog_1.resize(480,320)
    sys.exit(app.exec_())