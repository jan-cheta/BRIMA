from PySide6.QtWidgets import QDialog, QWidget, QHBoxLayout, QVBoxLayout,QFormLayout , QLineEdit, QDateEdit, QComboBox, QPushButton, QMessageBox, QLabel

class UpdateBar(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setObjectName('UpdateBar')
        layout = QHBoxLayout(self)
        
        self.btCancel = QPushButton('Cancel')
        self.btRevert = QPushButton('Revert')
        self.btUpdate = QPushButton('Save Changes')
        
        layout.addWidget(self.btCancel)
        layout.addStretch()
        layout.addWidget(self.btRevert)
        layout.addWidget(self.btUpdate)
    
class AddBar(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setObjectName('AddBar')
        layout = QHBoxLayout(self)
        
        self.btCancel = QPushButton('Cancel')
        self.btAdd = QPushButton('Add')
        
        layout.addWidget(self.btCancel)
        layout.addStretch()
        layout.addWidget(self.btAdd)
    
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
        
        main_layout = QVBoxLayout(self)
        
        self.header = QLabel('Add Household')
        self.form = HouseholdForm()
        self.addbar = AddBar()
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addWidget(self.addbar)
    
    def set_fields(self, **kargs):
        self.form.tbHouseholdName.setText(kargs['household_name'])
        self.form.tbHouseNo.setText(kargs['house_no'])
        self.form.tbStreet.setText(kargs['street'])
        self.form.cbSitio.setCurrentText(kargs['sitio'])
        self.form.tbLandmark.setText(kargs['landmark'])
    
    def get_fields(self):
        return {
            'household_name': self.form.tbHouseholdName.text(),
            'house_no': self.form.tbHouseNo.text(),
            'street': self.form.tbStreet.text(),
            'sitio': self.form.cbSitio.currentText(),
            'landmark': self.form.tbLandmark.text()
        }

class UpdateHouseholdForm(QDialog):
    def __init__(self):
        super().__init__()
        
        main_layout = QVBoxLayout(self)
        
        self.header = QLabel('Update Household')
        self.form = HouseholdForm()
        self.updatebar = UpdateBar()
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addWidget(self.updatebar)
    
    def set_fields(self, **kargs):
        self.form.tbHouseholdName.setText(kargs['household_name'])
        self.form.tbHouseNo.setText(kargs['house_no'])
        self.form.tbStreet.setText(kargs['street'])
        self.form.cbSitio.setCurrentText(kargs['sitio'])
        self.form.tbLandmark.setText(kargs['landmark'])
    
    def get_fields(self):
        return {
            'household_name': self.form.tbHouseholdName.text(),
            'house_no': self.form.tbHouseNo.text(),
            'street': self.form.tbStreet.text(),
            'sitio': self.form.cbSitio.currentText(),
            'landmark': self.form.tbLandmark.text()
        }