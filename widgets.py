from PySide6.QtWidgets import (QTableWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QLabel, QTableWidgetItem, QHeaderView)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt

class BaseWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        
        main_layout = QVBoxLayout(self)
        
        self.title = QLabel(title)
        
        main_layout.addWidget(self.title)
        
        top_bar = QWidget()
        top_bar.setObjectName('top_bar')
        top_bar_layout = QHBoxLayout(top_bar)
        
        icon_size = QSize(24, 24)
        
        self.btAdd = QPushButton("Add")
        self.btAdd.setObjectName("btAdd")
        self.btAdd.setIcon(QIcon(":/add"))
        self.btAdd.setIconSize(icon_size)
        self.btEdit = QPushButton("Edit")
        self.btEdit.setObjectName("btEdit")
        self.btEdit.setIcon(QIcon(":/edit"))
        self.btEdit.setIconSize(icon_size)
        self.btDelete = QPushButton("Delete")
        self.btDelete.setObjectName("btDelete")
        self.btDelete.setIcon(QIcon(":/delete"))
        self.btDelete.setIconSize(icon_size)
        self.btBrowse = QPushButton("Browse")
        self.btBrowse.setObjectName("btBrowse")
        self.btBrowse.setIcon(QIcon(":/browse"))
        self.btBrowse.setIconSize(icon_size)
        self.btRefresh = QPushButton("Refresh")
        self.btRefresh.setObjectName("btRefresh")
        self.btRefresh.setIcon(QIcon(":/refresh"))
        self.btRefresh.setIconSize(icon_size)
        
        top_bar_layout.addWidget(self.btAdd)
        top_bar_layout.addWidget(self.btEdit)
        top_bar_layout.addWidget(self.btDelete)
        top_bar_layout.addWidget(self.btBrowse)
        top_bar_layout.addWidget(self.btRefresh)
        top_bar_layout.addStretch()
        
        main_layout.addWidget(top_bar)
        
        search = QWidget()
        search.setObjectName('searchbar')
        search_layout = QHBoxLayout(search)
        
        self.tbSearchBar = QLineEdit()
        self.tbSearchBar.setObjectName('tbSearchBar')
        self.btSearch = QPushButton("Search")
        self.btSearch.setIconSize(icon_size)
        self.btSearch.setObjectName('btSearch')
        self.btSearch.setIcon(QIcon(":/search"))
        
        search_layout.addWidget(self.tbSearchBar)
        search_layout.addWidget(self.btSearch)
        
        main_layout.addWidget(search)
        
        self.table = QTableWidget()
        self.table.setObjectName('table')
        
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        main_layout.addWidget(self.table)
        
    def load_table(self, headers, data):
        self.table.clearContents()
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(headers))
        self.table.setColumnHidden(0, True)
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)

        if not data:
            return
        
        for row, row_data in enumerate(data):
            for col, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)
    
    def get_table_row(self):
        selected_row = self.table.currentRow()
        return int(self.table.item(selected_row, 0).text())
        
    def get_search_text(self):
        return self.tbSearchBar.text()
    
    def set_search_text(self, text):
        self.tbSearchBar.setText(text)
    
    