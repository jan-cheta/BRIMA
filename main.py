from view import MainView
from controller import MainController
from PySide6.QtWidgets import QApplication, QDialog
from resources_rc import *
from wizard import InitWizard
from base import Database
from model import User
import sys

def main():
    app = QApplication([])
    
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
