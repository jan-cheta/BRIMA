from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QLineEdit, QFormLayout,
    QDateEdit, QComboBox, QDialog, QSpinBox, QCompleter
)
from PySide6.QtCore import Qt
from ui.forms.components import FormHeader, FilterBar, UpdateBar, AddBar

class ResidentForm(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QHBoxLayout(self)  # Use QVBoxLayout for main layout

        sidestack1 = QWidget()
        sidelayout1 = QVBoxLayout(sidestack1)
        # Personal Information Section
        personal_group = QGroupBox('Personal Information')
        personal_layout = QFormLayout()
        self.tbFirstName = QLineEdit()
        self.tbLastName = QLineEdit()
        self.tbMiddleName = QLineEdit()
        self.tbSuffix = QLineEdit()
        self.tbBirthDate = QDateEdit()
        self.tbBirthDate.setCalendarPopup(True)
        personal_layout.addRow('First Name:', self.tbFirstName)
        personal_layout.addRow('Last Name:', self.tbLastName)
        personal_layout.addRow('Middle Name:', self.tbMiddleName)
        personal_layout.addRow('Suffix:', self.tbSuffix)
        personal_layout.addRow('Birth Date:', self.tbBirthDate)
        personal_group.setLayout(personal_layout)
        sidelayout1.addWidget(personal_group)
        
        # Contact Information Section
        contact_group = QGroupBox('Contact Information')
        contact_layout = QFormLayout()
        self.tbPhone1 = QLineEdit()
        self.tbPhone2 = QLineEdit()
        self.tbEmail = QLineEdit()
        contact_layout.addRow('Phone 1:', self.tbPhone1)
        contact_layout.addRow('Phone 2:', self.tbPhone2)
        contact_layout.addRow('Email:', self.tbEmail)
        contact_group.setLayout(contact_layout)
        sidelayout1.addWidget(contact_group)
        

        sidestack2 = QWidget()
        sidelayout2 = QVBoxLayout(sidestack2)
        # Household Information Section
        household_group = QGroupBox('Household Information')
        household_layout = QFormLayout()
        self.cbHousehold = QComboBox()
        self.cbHousehold.setEditable(True)
        completer = self.cbHousehold.completer()
        completer.setFilterMode(Qt.MatchContains)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setCompletionMode(QCompleter.PopupCompletion) 
        self.cbHousehold.setCompleter(completer)
        self.cbHousehold.setInsertPolicy(QComboBox.NoInsert)
        self.tbHouseholdName = QLineEdit()
        self.tbHouseNo = QLineEdit()
        self.tbStreet = QLineEdit()
        self.cbSitio = QComboBox()
        self.cbSitio.addItems(['CASARATAN', 'CABAOANGAN', 'TRAMO'])
        self.tbLandmark = QLineEdit()
        self.tbHouseholdName.setReadOnly(True)
        self.tbHouseNo.setReadOnly(True)
        self.tbStreet.setReadOnly(True)
        self.cbSitio.setDisabled(True)
        self.tbLandmark.setReadOnly(True)
        household_layout.addRow('Household:', self.cbHousehold)
        household_layout.addRow('Household Name:', self.tbHouseholdName)
        household_layout.addRow('House Number:', self.tbHouseNo)
        household_layout.addRow('Street:', self.tbStreet)
        household_layout.addRow('Sitio:', self.cbSitio)
        household_layout.addRow('Landmark:', self.tbLandmark)
        household_group.setLayout(household_layout)
        sidelayout2.addWidget(household_group)

        # Other Information Section
        other_group = QGroupBox('Other Information')
        other_layout = QFormLayout()
        self.tbOccupation = QLineEdit()
        self.cbCivilStatus = QComboBox()
        self.cbCivilStatus.addItems(["SINGLE", "MARRIED", "DIVORCED", "SEPARATED", "WIDOWED"])
        self.tbCitizenship = QLineEdit('FILIPINO')
        self.cbSex = QComboBox()
        self.cbSex.addItems(['MALE', 'FEMALE', 'OTHER'])
        self.cbEducation = QComboBox()
        self.cbEducation.addItems(
            [
                'SOME ELEMENTARY',
                'ELEMENTARY GRADUATE',
                'SOME HIGH SCHOOL',
                'HIGH SCHOOL GRADUATE',
                'SOME COLLEGE/VOCATIONAL',
                'COLLEGE GRADUATE',
                "SOME/COMPLETED MASTER'S DEGREE",
                'MASTERS GRADUATE',
                'VOCATIONAL/TVET'
            ]
        )
        self.tbRemarks = QLineEdit()
        self.cbRole = QComboBox()
        self.cbRole.addItems(['HEAD', 'SPOUSE', 'CHILD'])
        other_layout.addRow('Occupation:', self.tbOccupation)
        other_layout.addRow('Civil Status:', self.cbCivilStatus)
        other_layout.addRow('Citizenship:', self.tbCitizenship)
        other_layout.addRow('Sex:', self.cbSex)
        other_layout.addRow('Education:', self.cbEducation)
        other_layout.addRow('Remarks:', self.tbRemarks)
        other_layout.addRow('Role:', self.cbRole)
        other_group.setLayout(other_layout)
        sidelayout2.addWidget(other_group)

        # Add sections to the main layout
        layout.addWidget(sidestack1)
        layout.addWidget(sidestack2)

class AddResidentForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Resident')
        
        self.setMinimumSize(600, 600)
        main_layout = QVBoxLayout(self)
    
        self.header = FormHeader('Add Resident')
        self.form = ResidentForm()
        self.addbar = AddBar()
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
        main_layout.addWidget(self.addbar)
        
    
class UpdateResidentForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Update Resident')
        self.setMinimumSize(600, 400)
        main_layout = QVBoxLayout(self)
        
        self.header = FormHeader('Update Resident')
        self.form = ResidentForm()
        self.updatebar = UpdateBar()
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
        main_layout.addWidget(self.updatebar)

class FilterResidentForm(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Filter Residents')
        self.setMinimumSize(600, 400)
        main_layout = QVBoxLayout(self)

        self.header = FormHeader('Filter Residents')
        self.form = QWidget()
        form_layout = QFormLayout(self.form)
        self.filterbar = FilterBar()

        age_widget = QWidget()
        age_widget_layout = QHBoxLayout(age_widget)
        self.tbStartAge = QSpinBox()
        self.tbEndAge = QSpinBox()
        age_widget_layout.addWidget(self.tbStartAge)
        age_widget_layout.addWidget(self.tbEndAge)
        self.cbSitio = QComboBox()
        self.cbSitio.addItems(['','CASARATAN', 'CABAOANGAN', 'TRAMO'])
        self.cbCivilStatus = QComboBox()
        self.cbCivilStatus.addItems(["", "SINGLE", "MARRIED", "DIVORCED", "SEPARATED", "WIDOWED"])
        self.cbSex = QComboBox()
        self.cbSex.addItems(['','MALE', 'FEMALE', 'OTHER'])
        self.cbEducation = QComboBox()
        self.cbEducation.addItems(
            [
                '',
                'SOME ELEMENTARY',
                'ELEMENTARY GRADUATE',
                'SOME HIGH SCHOOL',
                'HIGH SCHOOL GRADUATE',
                'SOME COLLEGE/VOCATIONAL',
                'COLLEGE GRADUATE',
                "SOME/COMPLETED MASTER'S DEGREE",
                'MASTERS GRADUATE',
                'VOCATIONAL/TVET'
            ]
        )
        self.cbRole = QComboBox()
        self.cbRole.addItems(['','HEAD', 'SPOUSE', 'CHILD'])

        form_layout.addRow("Age Range: ",age_widget)
        form_layout.addRow("Sitio : ", self.cbSitio)
        form_layout.addRow("Civil Status: ", self.cbCivilStatus)
        form_layout.addRow("Sex: ", self.cbSex)
        form_layout.addRow("Education: ", self.cbEducation)
        form_layout.addRow("Role: ", self.cbRole)
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
        main_layout.addWidget(self.filterbar)