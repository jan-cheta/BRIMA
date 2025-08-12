from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget 
)
from ui.forms.components import AddBar, UpdateBar 

class AddForm(QDialog):
    def __init__(self):
        super().__init__()
        self._set_window_title()

        self.setMinimumSize(600, 400)
        
        main_layout = QVBoxLayout(self)
        
        self.header = self._set_header()

        self.form = self._set_form()
        self.addbar = AddBar()
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
        main_layout.addWidget(self.addbar)

    def _set_window_title(self):
        pass

    def _set_header(self):
        pass

    def _set_form(self):
        pass

class UpdateForm(QDialog):
    def __init__(self):
        super().__init__()
        self._set_window_title()

        self.setMinimumSize(600, 400)

        main_layout = QVBoxLayout(self)
        
        self.header = self._set_header()
        self.form = self._set_form()
        self.updatebar = UpdateBar()
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
        main_layout.addWidget(self.updatebar)

    def _set_window_title(self):
        pass

    def _set_header(self):
        pass

    def _set_form(self):
        pass 

    
class BrowseForm(QDialog):
    def __init__(self):
        super().__init__()
        self._set_window_title()
        
        self.setMinimumSize(600, 400)

        main_layout = QVBoxLayout(self)

        self.header = self._set_header()
        self.form = self._set_form()
        
        self.table = QTableWidget()

        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        main_layout.addWidget(self.table)
        main_layout.addStretch()
    
    def _set_window_title(self):
        pass

    def _set_header(self):
        pass

    def _set_form(self):
        pass 

