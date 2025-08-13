from PySide6.QtWidgets import (QTableWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QLabel, QTableWidgetItem, QHeaderView, QGroupBox, QTextEdit, QFormLayout, QScrollArea)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt

import pyqtgraph as pg
from pyqtgraph import PlotWidget

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
        
        filter = QWidget()
        filter.setObjectName('filterbar')
        filter_layout = QHBoxLayout(filter)

        self.btFilter = QPushButton("Filters")
        self.btFilter.setCheckable(True)
        self.btFilter.setChecked(False)
        self.btFilter.setIcon(QIcon(":/filter_on"))
        self.btFilter.setIconSize(icon_size)

        self.lbFilter = QLabel("No Applied Filter")

        filter_layout.addWidget(self.btFilter)
        filter_layout.addWidget(self.lbFilter)
        filter_layout.addStretch()
        
        main_layout.addWidget(filter)
        
        self.table = QTableWidget()
        self.table.setObjectName('table')
        
        self.table.verticalHeader().setVisible(True)
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
    
    def set_filter_text(self, text):
        self.lbFilter.setText(text)

class AboutMember(QGroupBox):
    def __init__(self, member, position):
        super().__init__()

        main_layout = QFormLayout(self)

        self.tbMember = QLineEdit()
        self.tbMember.setReadOnly(True)
        self.tbPosition = QLineEdit()
        self.tbPosition.setReadOnly(True)

        main_layout.addRow('Official Name:', self.tbMember)
        main_layout.addRow('Position:', self.tbPosition)

        self.tbMember.setText(member)
        self.tbPosition.setText(position)

class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # Create the main layout for this widget
        main_layout = QVBoxLayout(self)
        
        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True) 
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Create a widget to hold the content that will be scrolled
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Add header to the scroll content
        self.header = QLabel("BRGY. SIBLOT")
        self.header.setStyleSheet("""
            QLabel {
            font-size: 20px;
            font-weight: bold;
            color: #2a61ad; /* a readable shade of blue */
            }
        """)
        self.header.setAlignment(Qt.AlignCenter)
        scroll_layout.addWidget(self.header)
        
        # History section
        self.history = QGroupBox("HISTORY")
        history_layout = QVBoxLayout()
        self.history_body = QTextEdit()
        self.history_body.setReadOnly(True)
        history_layout.addWidget(self.history_body)
        self.history.setLayout(history_layout)
        scroll_layout.addWidget(self.history)

        # Mission section
        self.mission = QGroupBox("MISSION")
        mission_layout = QVBoxLayout()
        self.mission_body = QTextEdit()
        self.mission_body.setReadOnly(True)
        mission_layout.addWidget(self.mission_body)
        self.mission.setLayout(mission_layout)
        scroll_layout.addWidget(self.mission)

        # Vision section
        self.vision = QGroupBox("VISION")
        vision_layout = QVBoxLayout()
        self.vision_body = QTextEdit()
        self.vision_body.setReadOnly(True)
        vision_layout.addWidget(self.vision_body)
        self.vision.setLayout(vision_layout)
        scroll_layout.addWidget(self.vision)

        # Members section
        self.members = QGroupBox("OFFICIALS")
        self.members_layout = QVBoxLayout()
        self.members.setLayout(self.members_layout)
        scroll_layout.addWidget(self.members)
        
        # Set the content widget to the scroll area
        scroll_area.setWidget(scroll_content)
        
        # Add the scroll area to the main layout
        main_layout.addWidget(scroll_area)
    
    def load_data(self, **kargs):
        self.header.setText(kargs.get('name', 'BARANGAY'))
        self.history_body.setText(kargs.get('history', ''))
        self.mission_body.setText(kargs.get('mission', ''))
        self.vision_body.setText(kargs.get('vision', ''))

        # Clear existing members
        while self.members_layout.count(): 
            w = self.members_layout.takeAt(0).widget()
            if w:
                w.deleteLater()

        # Add new members
        for member in kargs.get('members', []):
            self.members_layout.addWidget(AboutMember(member.get('name', ''), member.get('position', '')))


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True) 
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Create a widget to hold the content that will be scrolled
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Edit Barangay Information
        self.edit_barangay = QGroupBox()
        self.edit_barangay.setTitle('Edit Barangay Details')
        edit_barangay_layout = QVBoxLayout(self.edit_barangay)
        self.edit_barangay_form = QWidget()
        edit_barangay_form_layout = QFormLayout(self.edit_barangay_form)
        self.edit_barangay_buttons = QWidget()
        edit_barangay_buttons_layout = QHBoxLayout(self.edit_barangay_buttons)

        self.tbBarangayName = QLineEdit()
        self.tbHistory = QTextEdit()
        self.tbMission = QTextEdit()
        self.tbVision = QTextEdit()
        edit_barangay_form_layout.addRow('Barangay Name (Please Include Municipality/City): ', self.tbBarangayName)
        edit_barangay_form_layout.addRow('History: ', self.tbHistory)
        edit_barangay_form_layout.addRow('Mission: ', self.tbMission)
        edit_barangay_form_layout.addRow('Vision: ', self.tbVision)
        edit_barangay_layout.addWidget(self.edit_barangay_form)

        self.btSave = QPushButton('Save')
        self.btRevert = QPushButton('Revert')
        edit_barangay_buttons_layout.addStretch()
        edit_barangay_buttons_layout.addWidget(self.btRevert)
        edit_barangay_buttons_layout.addWidget(self.btSave)
        edit_barangay_layout.addWidget(self.edit_barangay_buttons)

        scroll_layout.addWidget(self.edit_barangay)

        # Export data to csv
        self.export_csv = QGroupBox('Export')
        export_csv_layout = QVBoxLayout(self.export_csv)

        self.btExport = QPushButton('Export Data to XLSX')
        export_csv_layout.addWidget(self.btExport)

        scroll_layout.addWidget(self.export_csv)

        #Database Backup
        self.backup = QGroupBox('Data Backup')
        backup_layout = QVBoxLayout(self.backup)
        self.warning_label = QLabel(
            "WARNING: Use the backup function only when the current database is broken."
        )
        self.btCreateBackup = QPushButton('Create Backup')
        self.btViewBackup = QPushButton('Switch to Backup')
        backup_layout.addWidget(self.warning_label)
        backup_layout.addWidget(self.btCreateBackup)
        backup_layout.addWidget(self.btViewBackup)

        scroll_layout.addWidget(self.backup)

        
        # Set the content widget to the scroll area
        scroll_area.setWidget(scroll_content)
        
        # Add the scroll area to the main layout
        main_layout.addWidget(scroll_area)

    def get_fields(self):
        return{
            "name": self.tbBarangayName.text(),
            "history": self.tbHistory.toPlainText(),
            "mission": self.tbMission.toPlainText(),
            "vision": self.tbVision.toPlainText()
        }

    def set_fields(self, **kargs):
        self.tbBarangayName.setText(kargs.get("name", ''))
        self.tbHistory.setText(kargs.get("history", ''))
        self.tbMission.setText(kargs.get("mission", ''))
        self.tbVision.setText(kargs.get("vision", ''))
                    

class DataPlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(400)
        self.setMinimumWidth(400)
        
        self.plot_widget = PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.showGrid(x=True, y=True)
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.plot_widget)
        
        self.bar_item = None
        self.text_items = []

class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Brima Dashboard")
        self.setMinimumSize(800, 600)

        main_layout = QVBoxLayout(self)

        self.title = QLabel("Dashboard")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #2a61ad;
            }
        """)
        main_layout.addWidget(self.title)

        self.plot_grid = pg.GraphicsLayoutWidget()
        self.plot_grid.setBackground('w')
        main_layout.addWidget(self.plot_grid)

        self.plot_items = []  # Store plot references for updates

        rows, cols = 3, 2  # 3 rows × 2 columns = 6 plots
        for row in range(rows):
            for col in range(cols):
                plot = self.plot_grid.addPlot(row=row, col=col)
                
                # Disable mouse interaction
                plot.setMouseEnabled(x=False, y=False)  # Disable panning
                plot.hideButtons()  # Hide the auto-scale button
                
                # Disable zooming
                for mouse_event in ['wheel', 'drag']:
                    plot.setMouseEnabled(x=False, y=False)
                
                # Set axis styles
                plot.showGrid(x=True, y=True)
                plot.setLabel('left', 'Count')
                plot.setTitle(f"Plot {row * cols + col + 1}")
                
                # Add padding to view box
                plot.vb.setLimits(xMin=-0.5, 
                                 xMax=3.5,  # Adjust based on number of bars
                                 yMin=0, 
                                 yMax=100)  # Adjust based on expected max value
                
                # Disable auto-range on mouse events
                plot.vb.setMouseEnabled(x=False, y=False)
                
                self.plot_items.append(plot)

    
