from view import BrimaView
from controller import MainController, LoginController
from PySide6.QtWidgets import QApplication, QDialog
from resources_rc import *
from forms import LoginForm
from wizard import InitWizard
from base import Database
from model import User
import sys



def main():
    app = QApplication([])
    
    db = Database()
    session = db.get_session()

    if session.query(User).all():
        login_form = LoginForm()
        login_controller = LoginController(login_form)
        login_form.exec()
        if login_form.result() == QDialog.Accepted:
            user = login_controller.user
            view = BrimaView()
            controller = MainController(view, user)
            view.showMaximized()
            sys.exit(app.exec())
    else:
        wizard = InitWizard(session)
        wizard.exec()

if __name__ == "__main__":
    main()
