from PySide6.QtWidgets import (QWidget, QStackedWidget, QFormLayout, QHBoxLayout, QVBoxLayout,
                               QLabel, QLineEdit, QComboBox, QDateEdit, QPushButton, QTableWidget, QTableWidgetItem)
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QPixmap, QFont

from widgets import BaseWindow, AboutWindow, SettingsWindow, DashboardWindow

class MainView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('BRIMA')
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
    
        self.stack = QStackedWidget()
        self.stack.setContentsMargins(0,0,0,0)
        self.brima = BrimaView()
        self.login = LoginView()
        self.stack.addWidget(self.login)
        self.stack.addWidget(self.brima)

        main_layout.addWidget(self.stack)

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
        self.icon_helper(self.btDashboard, ":/icnDashboardBlack")

        self.btAboutUs = QPushButton('About Us')        
        self.btAboutUs.setObjectName('btAboutUs')
        self.icon_helper(self.btAboutUs, ":/icnAboutBlack")

        self.btHousehold = QPushButton('Household')
        self.btHousehold.setObjectName('btHousehold')
        self.icon_helper(self.btHousehold, ":/icnHouseholdBlack")

        self.btResident = QPushButton('Resident')
        self.btResident.setObjectName('btResident')
        self.icon_helper(self.btResident, ":/icnResidentsBlack")

        self.btBlotter = QPushButton('Blotter')
        self.btBlotter.setObjectName('btBlotter')
        self.icon_helper(self.btBlotter, ":/icnBlotterBlack")

        self.btCertificate = QPushButton('Certificate')
        self.btCertificate.setObjectName('btCertificate')
        self.icon_helper(self.btCertificate, ':/icnCertificateBlack')

        self.btAdmin = QPushButton('Admin')
        self.btAdmin.setObjectName('btAdmin')
        self.icon_helper(self.btAdmin, ':/icnAdminBlack')
        
        self.btSettings = QPushButton('Settings')
        self.btSettings.setObjectName('btSettings')
        self.icon_helper(self.btSettings, ':/icnSettingsBlack')

        self.btLogout = QPushButton('Logout')
        self.btLogout.setObjectName('btLogout')
        self.icon_helper(self.btLogout, ':/icnLogoutBlack')

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
        
        self.certificate_window = BaseWindow("Certificate")
        self.stack.addWidget(self.certificate_window)
    
        self.about_window = AboutWindow()
        self.stack.addWidget(self.about_window)

        self.settings_window = SettingsWindow()
        self.stack.addWidget(self.settings_window)

        self.dashboard_window = DashboardWindow()
        self.stack.addWidget(self.dashboard_window)

        content_layout.addWidget(self.stack)

        # Content Integration to Main Layout
        main_layout.addWidget(content)
    
    def icon_helper(self, button, path):
        icon_size = QSize(24, 24)
        
        button.setIcon(QIcon(path))
        button.setIconSize(icon_size)


class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        lbLogo = QLabel()
        pxLogo = QPixmap(":/login") 
        scaled_pxLogo = pxLogo.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation) #
        lbLogo.setPixmap(scaled_pxLogo) 
        lbLogo.setAlignment(Qt.AlignCenter) 
            
        lbBRIMA = QLabel("BRIMA")
        lbBRIMA.setAlignment(Qt.AlignCenter) 
        lbBRIMA.setFont(QFont("Segoe UI", 48, QFont.Bold))  
        lbBrima = QLabel("Barangay Records and Information Management Application")
        lbBrima.setAlignment(Qt.AlignCenter) 
        lbBrima.setFont(QFont("Segoe UI", 12))


        form_widget = QWidget()
        layout = QFormLayout(form_widget) 
        form_widget.setContentsMargins(10, 10, 10, 10) 
        layout.setSpacing(15) 

        self.tbUsername = QLineEdit()
        self.tbUsername.setFixedHeight(40)
        self.tbUsername.setPlaceholderText("Enter username")

        password_widget = QWidget()
        password_layout = QHBoxLayout(password_widget) 
        self.tbPassword = QLineEdit() 
        self.tbPassword.setEchoMode(QLineEdit.EchoMode.Password) 
        self.tbPassword.setFixedHeight(40)
        self.tbPassword.setPlaceholderText("Enter password")
        self.btShowPassword = QPushButton("Show") 
        self.btShowPassword.setMaximumWidth(60) 
        self.btShowPassword.setCheckable(True)
        self.btShowPassword.setFixedHeight(40)
        password_layout.addWidget(self.tbPassword) 
        password_layout.addWidget(self.btShowPassword)
        password_layout.setContentsMargins(0, 0, 0, 0) 

        layout.addRow("Username: ", self.tbUsername)
        layout.addRow("Password: ", password_widget)

        login_button_widget = QWidget()
        login_button_layout = QHBoxLayout(login_button_widget)
        self.btLogin = QPushButton("Login")
        self.btLogin.setFixedSize(200, 45)
        self.btLogin.setFont(QFont("Segoe UI", 15, QFont.Bold))
        login_button_layout.addWidget(self.btLogin)
        login_button_layout.setAlignment(Qt.AlignCenter) 
        login_button_layout.setContentsMargins(0, 0, 0, 0)
        

        self.setWindowTitle("Brima")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(0)
        main_layout.addStretch()
        main_layout.addWidget(lbLogo)
        main_layout.addWidget(lbBRIMA)
        main_layout.addWidget(lbBrima)
        main_layout.addWidget(form_widget)
        main_layout.addWidget(login_button_widget)
        main_layout.addStretch()


        self.btShowPassword.clicked.connect(lambda: self._show_pass(self.btShowPassword, self.tbPassword))

    def _show_pass(self, button : QPushButton, textbox : QLineEdit):
        if button.isChecked():
            button.setText("Hide")
            textbox.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            button.setText("Show")
            textbox.setEchoMode(QLineEdit.EchoMode.Password)   

    def get_fields(self):
        return{
            'username': self.tbUsername.text(),
            'password': self.tbPassword.text()
        }