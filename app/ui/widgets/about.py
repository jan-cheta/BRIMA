from PySide6.QtWidgets import (
    QGroupBox, QFormLayout, QLineEdit, QWidget, QVBoxLayout, QScrollArea,
    QTextEdit, QLabel
)

from PySide6.QtCore import Qt

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