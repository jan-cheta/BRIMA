from PySide6.QtWidgets import (QWidget, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, 
                               QDateEdit, QVBoxLayout, QHBoxLayout, QFormLayout, QDialog, QHeaderView)

from PySide6.QtCore import Signal


class CustomTable(QTableWidget):
    edit_clicked = Signal(int)
    delete_clicked = Signal(int)

    def __init__(self):
        super().__init__()
        self.data = None
        self.headers = None
        self.row_count = 15
        self.column_count = None
        self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.verticalHeader().setVisible(False)

    def setData(self, data):
        self.data = data
    
    def setHeader(self, header):
        self.headers = header.extend(['View', 'Edit', 'Delete'])
        self.column_count = len(header)
    
    def populateTable(self):
        self.clear()






class CustomWindow(QWidget):
    pass


class CustomForm(QDialog):
    pass

class ResidentForm(QDialog):
    pass
