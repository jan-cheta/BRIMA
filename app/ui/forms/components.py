from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

class FormHeader(QLabel):
    def __init__(self, title):
        super().__init__()

        self.setText(title)
        
        self.setAlignment(Qt.AlignCenter) 
        self.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: white;
            padding: 10px;
            background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 #3498db,
            stop: 1 #2c3e50
            );
            """)

class UpdateBar(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setObjectName('UpdateBar')
        layout = QHBoxLayout(self)
        
        self.btCancel = QPushButton('Cancel')
        self.btRevert = QPushButton('Revert')
        self.btUpdate = QPushButton('Save Changes')
        
        layout.addWidget(self.btCancel)
        layout.addStretch()
        layout.addWidget(self.btRevert)
        layout.addWidget(self.btUpdate)

class FilterBar(UpdateBar):
    def __init__(self):
        super().__init__()

        self.btRevert.setText('Clear Filter')
        self.btUpdate.setText('Apply Filter')    

class AddBar(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setObjectName('AddBar')
        layout = QHBoxLayout(self)
        
        self.btCancel = QPushButton('Cancel')
        self.btAdd = QPushButton('Add')
        
        layout.addWidget(self.btCancel)
        layout.addStretch()
        layout.addWidget(self.btAdd)