from PySide6.QtWidgets import (QWidget, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, 
                               QDateEdit, QVBoxLayout, QHBoxLayout, QFormLayout, QDialog, QHeaderView)


class CustomTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.data = None
        self.headers = None

    def setData(self, data):
        self.data = data
    
    def setHeader(self, header):
        self.headers = header
    
    def populateTable(self):
        self.clear()



class CustomWindow(QWidget):
    pass

class CustomForm(QDialog):
    pass

class ResidentForm(QDialog):
    pass
