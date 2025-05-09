from PySide6.QtWidgets import (QGridLayout, QTableWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QLabel, QTableWidgetItem, QHeaderView, QGroupBox, QTextEdit, QFormLayout, QScrollArea)
from PySide6.QtGui import QIcon, QPainter, QPixmap, QImage
from PySide6.QtCore import QSize, Qt, QRect
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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



class ScalableImageWidget(QWidget):
    
    def __init__(self, image_path: str, parent=None):
        super().__init__(parent)
        self.original_pixmap = QPixmap(image_path)
        self.scaled_pixmap = None
        self.setMinimumSize(10, 10)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.original_pixmap.isNull():
            self.scaled_pixmap = self.original_pixmap.scaled(
                self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        self.update()

    def paintEvent(self, event):
        if self.scaled_pixmap:
            painter = QPainter(self)
            # Center the scaled pixmap inside the widget
            x = (self.width() - self.scaled_pixmap.width()) // 2
            y = (self.height() - self.scaled_pixmap.height()) // 2
            target_rect = QRect(x, y, self.scaled_pixmap.width(), self.scaled_pixmap.height())
            painter.drawPixmap(target_rect, self.scaled_pixmap)
            painter.end()
            

class ChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot_data(self, labels, values, title="Resident Stats"):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(labels, values)
        ax.set_title(title)
        self.canvas.draw()
        
# TODO:
class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        main_layout = QGridLayout(self)
        
        