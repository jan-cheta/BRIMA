from PySide6.QtWidgets import (QWidget, QStackedWidget, QFormLayout, QHBoxLayout, QVBoxLayout,
                               QLabel, QLineEdit, QComboBox, QDateEdit, QPushButton, QTableWidget, QTableWidgetItem)
from widgets import BaseWindow

class BrimaView(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)

        # Header
        header = QWidget()
        header.setObjectName('header')
        header_layout = QHBoxLayout(header)

        self.lbBrima = QLabel('BRIMA')
        self.lbBrima.setObjectName('lbBrima')
        self.lbBrgy = QLabel('BRGY. SIBLOT, SAN NICOLAS, PANGASINAN')
        self.lbBrgy.setObjectName('lbBrgy')
        self.lbUser = QLabel('HI, USER')
        self.lbUser.setObjectName('lbUser')

        header_layout.addWidget(self.lbBrima)
        header_layout.addStretch()
        header_layout.addWidget(self.lbBrgy)
        header_layout.addStretch()
        header_layout.addWidget(self.lbUser)

        main_layout.addWidget(header)

        # Wrapper for Sidebar and Window
        content = QWidget()
        content.setObjectName('content')
        content_layout = QHBoxLayout(content)

        # Sidebar
        sidebar = QWidget()
        sidebar.setObjectName('sidebar')
        sidebar_layout = QVBoxLayout(sidebar)

        self.btDashboard = QPushButton('Dahsboard')
        self.btDashboard.setObjectName('btDashboard')
        self.btAboutUs = QPushButton('About Us')
        self.btAboutUs.setObjectName('btAboutUs')
        self.btHousehold = QPushButton('Household')
        self.btHousehold.setObjectName('btHousehold')
        self.btResident = QPushButton('Resident')
        self.btResident.setObjectName('btResident')
        self.btBlotter = QPushButton('Blotter')
        self.btBlotter.setObjectName('btBlotter')
        self.btCertificate = QPushButton('Certificate')
        self.btCertificate.setObjectName('btCertificate')
        self.btAdmin = QPushButton('Admin')
        self.btAdmin.setObjectName('btAdmin')
        self.btSettings = QPushButton('Settings')
        self.btSettings.setObjectName('btSettings')
        self.btLogout = QPushButton('Logout')
        self.btLogout.setObjectName('btLogout')

        sidebar_layout.addWidget(self.btDashboard)
        sidebar_layout.addWidget(self.btAboutUs)
        sidebar_layout.addWidget(self.btHousehold)
        sidebar_layout.addWidget(self.btResident)
        sidebar_layout.addWidget(self.btBlotter)
        sidebar_layout.addWidget(self.btCertificate)
        sidebar_layout.addWidget(self.btAdmin)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.btSettings)
        sidebar_layout.addWidget(self.btLogout)

        content_layout.addWidget(sidebar)

        # ---Windows Stack---
        self.stack = QStackedWidget()
        self.stack.setObjectName('stack')
        
        self.household_window = BaseWindow("Household")
        self.stack.addWidget(self.household_window)
        
        self.resident_window = BaseWindow("Resident")
        self.stack.addWidget(self.resident_window)
        
        self.admin_window = BaseWindow("User")
        self.stack.addWidget(self.admin_window)
        
        self.blotter_window = BaseWindow("Blotter")
        self.stack.addWidget(self.blotter_window)

        content_layout.addWidget(self.stack)

        # Content Integration to Main Layout
        main_layout.addWidget(content)



    
