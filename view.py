from PySide6.QtWidgets import (QWidget, QStackedWidget, QFormLayout, QHBoxLayout, QVBoxLayout,
                               QLabel, QLineEdit, QComboBox, QDateEdit, QPushButton, QTableWidget, QWidgetItem) 

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

        sidebar_layout.addWidget(self.btDashboard)
        sidebar_layout.addWidget(self.btAboutUs)
        sidebar_layout.addWidget(self.btHousehold)
        sidebar_layout.addWidget(self.btResident)
        sidebar_layout.addWidget(self.btBlotter)
        sidebar_layout.addWidget(self.btCertificate)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.btAdmin)
        sidebar_layout.addWidget(self.btSettings)

        content_layout.addWidget(sidebar)

        # ---Windows Stack---
        self.stack = QStackedWidget()
        self.stack.setObjectName('stack')

        # TODO: ---Dashboard Window---
        self.wdDashboard = QWidget()
        self.wdDashboard.setObjectName('wdDashboard')

        # TODO: ---About Us Window---
        self.wdAboutUs = QWidget()
        self.wdAboutUs.setObjectName('wdAboutUs')
        # ---Household Windows---
        
        # Main Window
        self.wdHousehold = QWidget()
        self.wdHousehold.setObjectName('wdHousehold')
        wdHousehold_layout = QVBoxLayout(self.wdHousehold)

        self.lbHouseholdTitle = QLabel('Households')
        self.lbHouseholdTitle.setObjectName('lbHouseholdTitle')

        searchbar = QWidget()
        searchbar.setObjectName('searchbar')
        searchbar_layout = QHBoxLayout(searchbar)





        # Add Window


        # Edit Window

        # View Window

        content_layout.addWidget(self.stack)

        # Content Integration to Main Layout
        main_layout.addWidget(content)



    
