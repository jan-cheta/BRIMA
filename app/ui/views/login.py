from PySide6.QtWidgets import (
QWidget, QLabel, QFormLayout, QLineEdit, QHBoxLayout, QPushButton, QVBoxLayout
)

from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt

class LoginView(QWidget):
    def __init__(self):
        super().__init__()

        lbLogo = QLabel()
        pxLogo = QPixmap(":/login") 
        scaled_pxLogo = pxLogo.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation) #
        lbLogo.setPixmap(scaled_pxLogo) 
        lbLogo.setAlignment(Qt.AlignCenter) 
            
        lbBRIMA = QLabel("BRIMA")
        lbBRIMA.setObjectName("lbBrimaLogin")
        lbBRIMA.setAlignment(Qt.AlignCenter) 
        lbBrima = QLabel("Barangay Records and Information Management Application")
        lbBrima.setObjectName("lbFullBrimaLogin")
        lbBrima.setAlignment(Qt.AlignCenter) 

        form_widget = QWidget()
        layout = QFormLayout(form_widget) 
        form_widget.setObjectName("formWidget")
        form_widget.setContentsMargins(10, 10, 10, 10) 
        layout.setSpacing(15) 

        self.tbUsername = QLineEdit()
        self.tbUsername.setFixedHeight(40)
        self.tbUsername.setPlaceholderText("Enter username")

        password_widget = QWidget()
        password_layout = QHBoxLayout(password_widget) 
        password_widget.setObjectName("passwordWidget")
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
        login_button_widget.setObjectName("loginButtonWidget")
        login_button_layout = QHBoxLayout(login_button_widget)
        self.btLogin = QPushButton("Login")
        self.btLogin.setObjectName("btLogin")
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