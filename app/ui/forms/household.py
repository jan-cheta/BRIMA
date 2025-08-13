from PySide6.QtWidgets import (
    QWidget, QDialog, QFormLayout, QLineEdit, QComboBox,
    QVBoxLayout, QTableWidget
)

from ui.forms.components import FormHeader, FilterBar, AddBar, UpdateBar

class HouseholdForm(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setObjectName('HouseholdForm')
        layout = QFormLayout(self)
        
        self.tbHouseholdName = QLineEdit()
        self.tbHouseNo = QLineEdit()
        self.tbStreet = QLineEdit()
        self.cbSitio = QComboBox()
        self.cbSitio.addItems(['CASARATAN', 'CABAOANGAN', 'TRAMO'])
        self.tbLandmark = QLineEdit()
        
        layout.addRow('Household Name:', self.tbHouseholdName)
        layout.addRow('House No:', self.tbHouseNo)
        layout.addRow('Street:', self.tbStreet)
        layout.addRow('Sitio:', self.cbSitio)
        layout.addRow('Landmark:', self.tbLandmark)
        
class AddHouseholdForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Household')

        self.setMinimumSize(600, 400)
        
        main_layout = QVBoxLayout(self)
        
        self.header = FormHeader('Add Household')

        self.form = HouseholdForm()
        self.addbar = AddBar()
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
        main_layout.addWidget(self.addbar)
    

class UpdateHouseholdForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Update Household')

        self.setMinimumSize(600, 400)

        main_layout = QVBoxLayout(self)
        
        self.header = FormHeader('Update Household')
        self.form = HouseholdForm()
        self.updatebar = UpdateBar()
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
        main_layout.addWidget(self.updatebar)
    
    
class BrowseHouseholdForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Browse Household')
        
        self.setMinimumSize(600, 400)

        main_layout = QVBoxLayout(self)

        self.header = FormHeader('Browse Household')
        self.form = HouseholdForm()
        
        self.form.tbHouseholdName.setReadOnly(True)
        self.form.tbHouseNo.setReadOnly(True)
        self.form.tbStreet.setReadOnly(True)
        self.form.cbSitio.setDisabled(True)
        self.form.tbLandmark.setReadOnly(True)

        self.table = QTableWidget()

        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        main_layout.addWidget(self.table)
        main_layout.addStretch()

class FilterHouseholdForm(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Filter Households')
        main_layout = QVBoxLayout(self)

        self.header = FormHeader('Filter Households')
        self.form = QWidget()
        form_layout = QFormLayout(self.form)
        self.filterbar = FilterBar()
        self.cbSitio = QComboBox()
        self.cbSitio.addItems(['','CASARATAN', 'CABAOANGAN', 'TRAMO'])

        form_layout.addRow("Sitio", self.cbSitio)
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
        main_layout.addWidget(self.filterbar)