from view import BrimaView
from controller import HouseholdWindowController, MainController
from PySide6.QtWidgets import QApplication
from resources_rc import *
import sys



def main():
    app = QApplication([])
    view = BrimaView()
    controller = MainController(view)
    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

