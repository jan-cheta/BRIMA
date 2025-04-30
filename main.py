from view import BrimaView
from PySide6.QtWidgets import QApplication
import sys



def main():
    app = QApplication([])
    view = BrimaView()
    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

