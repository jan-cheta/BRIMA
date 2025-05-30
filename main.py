from view import MainView
from controller import MainController
from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtGui import QIcon
from PySide6.QtCore import QFile, QTextStream
from resources_rc import *
from wizard import InitWizard
from base import Database
from model import User
import sys

def main():
    app = QApplication([])
    app.setWindowIcon(QIcon(':/login'))
     # Load QSS
    file = QFile(":/styles")
    if file.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(file)
        app.setStyleSheet(stream.readAll())

    db = Database()
    session = db.get_session()

    if session.query(User).all():
        main_view = MainView()
        main_control = MainController(main_view)
        main_view.show()
        sys.exit(app.exec())
    else:
        wizard = InitWizard(session)
        wizard.exec()

if __name__ == "__main__":
    main()
