from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QStackedWidget
)

from ui.views.brima import BrimaView
from ui.views.login import LoginView

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