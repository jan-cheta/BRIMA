from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QPushButton, QHBoxLayout, QLineEdit
)

from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

class BaseWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        
        main_layout = QVBoxLayout(self)
        
        self.title = QLabel(title)
        self.title.setStyleSheet("""
            QLabel {
            font-size: 20px;
            font-weight: bold;
            color: #2a61ad; /* a readable shade of blue */
            }
        """)
        
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
        self.lbTotal = QLabel("Total: ")

        top_bar_layout.addWidget(self.btAdd)
        top_bar_layout.addWidget(self.btEdit)
        top_bar_layout.addWidget(self.btDelete)
        top_bar_layout.addWidget(self.btBrowse)
        top_bar_layout.addWidget(self.btRefresh)
        top_bar_layout.addWidget(self.lbTotal)
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
        
        filter_bar = QWidget()
        filter_layout = QHBoxLayout(filter_bar)

        self.btFilter = QPushButton("Filter")
        self.btFilter.setIcon(QIcon(":/filter"))
        self.lbActiveFilters = QLabel("No active filters")

        filter_layout.addWidget(self.btFilter)
        filter_layout.addWidget(self.lbActiveFilters)

        main_layout.addWidget(filter_bar)
        
        self.table = QTableWidget()
        self.table.setObjectName('table')
        
        self.table.verticalHeader().setVisible(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        main_layout.addWidget(self.table)