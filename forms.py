from datetime import date
from PySide6.QtWidgets import (QDialog, QGridLayout, QGroupBox, QTextEdit, QWidget, QHBoxLayout, QVBoxLayout,QFormLayout , QLineEdit,
    QDateEdit, QComboBox, QPushButton, QMessageBox, QLabel, QCompleter, QTableWidget, QTableWidgetItem, QHeaderView,
    QTextEdit)
from PySide6.QtCore import Qt, QDate, QSize
from PySide6.QtGui import QIcon, QPixmap, QFont

class TableForm(QWidget):
    def __init__(self):
        super().__init__()
        
        main_layout = QVBoxLayout(self)
        
        search = QWidget()
        search.setObjectName('searchbar')
        search_layout = QHBoxLayout(search)
        
        icon_size = QSize(24, 24)
        
        self.tbSearchBar = QLineEdit()
        self.tbSearchBar.setObjectName('tbSearchBar')
        self.btSearch = QPushButton("Search")
        self.btSearch.setIconSize(icon_size)
        self.btSearch.setObjectName('btSearch')
        self.btSearch.setIcon(QIcon(":/search"))
        
        search_layout.addWidget(self.tbSearchBar)
        search_layout.addWidget(self.btSearch)
        
        self.table = QTableWidget()
        self.table.setObjectName('table')
        
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    
        main_layout.addWidget(search)
        main_layout.addWidget(self.table)
        
    def load_table(self, headers, data):
        self.table.clearContents()
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(headers))
        self.table.setColumnHidden(0, True)
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)

        if not data:
            return
        
        for row, row_data in enumerate(data):
            for col, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)
    
    def get_table_row(self):
        selected_row = self.table.currentRow()
        return int(self.table.item(selected_row, 0).text())
        
    def get_search_text(self):
        return self.tbSearchBar.text()
    
    def set_search_text(self, text):
        self.tbSearchBar.setText(text)
        
        

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
        self.setWindowTitle('Add Household')

        self.setMinimumSize(600, 400)
        
        main_layout = QVBoxLayout(self)
        
        self.header = QLabel('Add Household')
        self.header.setAlignment(Qt.AlignCenter) 
        self.header.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
            padding: 10px;
        """)
        self.form = HouseholdForm()
        self.addbar = AddBar()
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
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
        self.setWindowTitle('Update Household')

        self.setMinimumSize(600, 400)

        main_layout = QVBoxLayout(self)
        
        self.header = QLabel('Update Household')
        self.header.setAlignment(Qt.AlignCenter) 
        self.header.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
            padding: 10px;
        """)
        self.form = HouseholdForm()
        self.updatebar = UpdateBar()
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
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
    
class BrowseHouseholdForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Browse Household')
        
        self.setMinimumSize(600, 400)

        main_layout = QVBoxLayout(self)
        
        self.header = QLabel('Browse Household')
        self.header.setAlignment(Qt.AlignCenter) 
        self.header.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
            padding: 10px;
        """)
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


    def load_table(self, headers, data):
        self.table.clearContents()
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(headers))
        self.table.setColumnHidden(0, True)
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)

        if not data:
            return
        
        for row, row_data in enumerate(data):
            for col, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)
    
    def set_fields(self, **kargs):
        self.form.tbHouseholdName.setText(kargs['household_name'])
        self.form.tbHouseNo.setText(kargs['house_no'])
        self.form.tbStreet.setText(kargs['street'])
        self.form.cbSitio.setCurrentText(kargs['sitio'])
        self.form.tbLandmark.setText(kargs['landmark'])
    
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
        self.tbCitizenship = QLineEdit()
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
        self.cbRole.addItems(['Head', 'Spouse', 'Child'])
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
        
        self.setMinimumSize(600, 400)
        main_layout = QVBoxLayout(self)
    
        self.header = QLabel('Add Resident')
        self.header.setAlignment(Qt.AlignCenter) 
        self.header.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
            padding: 10px;
        """)
        self.form = ResidentForm()
        self.addbar = AddBar()
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
        main_layout.addWidget(self.addbar)
        
    def set_fields(self, **kargs):
        self.form.cbHousehold.addItems(kargs['household'])
    
    def get_fields(self):
        return {
            'first_name' : self.form.tbFirstName.text(),
            'last_name' : self.form.tbLastName.text(),
            'middle_name' : self.form.tbMiddleName.text(),
            'suffix' : self.form.tbSuffix.text(),
            'date_of_birth' : self.form.tbBirthDate.date().toPython(),
            'phone1' : self.form.tbPhone1.text(),
            'phone2' : self.form.tbPhone2.text(),
            'email' : self.form.tbEmail.text(),
            'household' : self.form.cbHousehold.currentText(),
            'occupation' : self.form.tbOccupation.text(),
            'civil_status' : self.form.cbCivilStatus.currentText(),
            'citizenship' : self.form.tbCitizenship.text(),
            'sex': self.form.cbSex.currentText(),
            'education': self.form.cbEducation.currentText(),
            'remarks': self.form.tbRemarks.text(),
            'role': self.form.cbRole.currentText()
        }
    
class UpdateResidentForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Update Resident')
        self.setMinimumSize(600, 400)
        main_layout = QVBoxLayout(self)
        
        self.header = QLabel('Update Resident')
        self.header.setAlignment(Qt.AlignCenter) 
        self.header.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
            padding: 10px;
        """)
        self.form = ResidentForm()
        self.updatebar = UpdateBar()
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
        main_layout.addWidget(self.updatebar)
        
    def set_fields(self, **kargs):
        
        self.form.tbFirstName.setText(kargs.get('first_name', ''))
        self.form.tbLastName.setText(kargs.get('last_name', ''))
        self.form.tbMiddleName.setText(kargs.get('middle_name', ''))
        self.form.tbSuffix.setText(kargs.get('suffix', ''))
        
        date_of_birth = kargs.get('date_of_birth', None)
        
        # If date_of_birth exists and is a date object, convert it to QDate
        if isinstance(date_of_birth, date):
            # Extract year, month, and day from the date object
            qdate_of_birth = QDate(date_of_birth.year, date_of_birth.month, date_of_birth.day)
        else:
            # Default to current date if no valid date is found
            qdate_of_birth = QDate.currentDate()
        
        # Set the value in the QDateEdit widget
        self.form.tbBirthDate.setDate(qdate_of_birth)
        self.form.tbPhone1.setText(kargs.get('phone1', ''))
        self.form.tbPhone2.setText(kargs.get('phone2', ''))
        self.form.tbEmail.setText(kargs.get('email', ''))
        self.form.cbHousehold.setCurrentText(kargs.get('household', ''))
        self.form.tbOccupation.setText(kargs.get('occupation', ''))
        self.form.cbCivilStatus.setCurrentText(kargs.get('civil_status', ''))
        self.form.cbSex.setCurrentText(kargs.get('sex', ''))
        self.form.cbEducation.setCurrentText(kargs.get('education', ''))
        self.form.tbCitizenship.setText(kargs.get('citizenship', ''))
        self.form.tbRemarks.setText(kargs.get('remarks', ''))
        self.form.cbRole.setCurrentText(kargs.get('role', ''))
    
    def get_fields(self):
        return {
            'first_name' : self.form.tbFirstName.text(),
            'last_name' : self.form.tbLastName.text(),
            'middle_name' : self.form.tbMiddleName.text(),
            'suffix' : self.form.tbSuffix.text(),
            'date_of_birth' : self.form.tbBirthDate.date().toPython(),
            'phone1' : self.form.tbPhone1.text(),
            'phone2' : self.form.tbPhone2.text(),
            'email' : self.form.tbEmail.text(),
            'household' : self.form.cbHousehold.currentText(),
            'occupation' : self.form.tbOccupation.text(),
            'civil_status' : self.form.cbCivilStatus.currentText(),
            'citizenship' : self.form.tbCitizenship.text(),
            'sex': self.form.cbSex.currentText(),
            'education': self.form.cbEducation.currentText(),
            'remarks': self.form.tbRemarks.text(),
            'role': self.form.cbRole.currentText()
        }

class BrowseResidentForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Browse Resident')
        self.setMinimumSize(600, 400)
        main_layout = QVBoxLayout(self)
        
        self.header = QLabel('Browse Resident')
        self.form = ResidentForm()
        
        self.form.tbFirstName.setReadOnly(True)
        self.form.tbLastName.setReadOnly(True)
        self.form.tbMiddleName.setReadOnly(True)
        self.form.tbSuffix.setReadOnly(True)
        self.form.tbBirthDate.setReadOnly(True)
        self.form.tbPhone1.setReadOnly(True)
        self.form.tbPhone2.setReadOnly(True)
        self.form.tbEmail.setReadOnly(True)
        self.form.cbHousehold.setDisabled(True)
        self.form.tbOccupation.setReadOnly(True)
        self.form.cbCivilStatus.setDisabled(True)
        self.form.cbSex.setDisabled(True)
        self.form.cbEducation.setDisabled(True)
        self.form.tbRemarks.setReadOnly(True)
        self.form.cbRole.setDisabled(True)
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
        
    def set_fields(self, **kargs):
        self.form.tbFirstName.setText(kargs.get('first_name', ''))
        self.form.tbLastName.setText(kargs.get('last_name', ''))
        self.form.tbMiddleName.setText(kargs.get('middle_name', ''))
        self.form.tbSuffix.setText(kargs.get('suffix', ''))
        
        date_of_birth = kargs.get('date_of_birth', None)
        
        # If date_of_birth exists and is a date object, convert it to QDate
        if isinstance(date_of_birth, date):
            # Extract year, month, and day from the date object
            qdate_of_birth = QDate(date_of_birth.year, date_of_birth.month, date_of_birth.day)
        else:
            # Default to current date if no valid date is found
            qdate_of_birth = QDate.currentDate()
        
        # Set the value in the QDateEdit widget
        self.form.tbBirthDate.setDate(qdate_of_birth)
        self.form.tbPhone1.setText(kargs.get('phone1', ''))
        self.form.tbPhone2.setText(kargs.get('phone2', ''))
        self.form.tbEmail.setText(kargs.get('email', ''))
        self.form.cbHousehold.setCurrentText(kargs.get('household', ''))
        self.form.tbOccupation.setText(kargs.get('occupation', ''))
        self.form.cbCivilStatus.setCurrentText(kargs.get('civil_status', ''))
        self.form.tbCitizenship.setText(kargs.get('citizenship', ''))
        self.form.cbSex.setCurrentText(kargs.get('sex', ''))
        self.form.cbEducation.setCurrentText(kargs.get('education', ''))
        self.form.tbRemarks.setText(kargs.get('remarks', ''))
        self.form.cbRole.setCurrentText(kargs.get('role', ''))
        
class UserForm(QWidget):
    def __init__(self):
        super().__init__()
        
        main_layout = QFormLayout(self)
        
        self.cbName = QComboBox()
        self.cbName.setEditable(True)
        completer = self.cbName.completer()
        completer.setFilterMode(Qt.MatchContains)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setCompletionMode(QCompleter.PopupCompletion) 
        self.cbName.setCompleter(completer)
        self.cbName.setInsertPolicy(QComboBox.NoInsert)
        
        self.tbUserName = QLineEdit()
        self.tbPassword = QLineEdit()
        self.tbConfirmPassword = QLineEdit()
        self.tbPassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.tbConfirmPassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.cbPosition = QComboBox()
        self.cbPosition.addItems(["CAPTAIN", "SECRETARY", "TREASURER", "KAGAWAD", "TANOD"])
        
        main_layout.addRow('Name:', self.cbName)
        main_layout.addRow('User Name:', self.tbUserName)
        main_layout.addRow('Password:', self.tbPassword)
        main_layout.addRow('Confirm Password', self.tbConfirmPassword)
        main_layout.addRow('Position:', self.cbPosition)

class AddUserForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add User')
        self.setMinimumSize(600, 400)
        main_layout = QVBoxLayout(self)
        
        self.header = QLabel('Add User')
        self.form = UserForm()
        self.addbar = AddBar()
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
        main_layout.addWidget(self.addbar)
        
    def set_fields(self, **kargs):
        self.form.cbName.addItems(kargs.get('name', ''))
    
    def get_fields(self):
        return {
            'name' : self.form.cbName.currentText(),
            'username' : self.form.tbUserName.text(),
            'password' : self.form.tbPassword.text(),
            'confirm_password': self.form.tbConfirmPassword.text(),
            'position' : self.form.cbPosition.currentText()
        }
        
class UpdateUserForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Update User')
        self.setMinimumSize(600, 400)
        main_layout = QVBoxLayout(self)
        
        self.header = QLabel('Update User')
        self.form = UserForm()
        self.updatebar = UpdateBar()
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
        main_layout.addWidget(self.updatebar)
        
    def set_fields(self, **kargs):
        self.form.cbName.setCurrentText(kargs.get('name', ''))
        self.form.tbUserName.setText(kargs.get('username', ''))
        self.form.tbPassword.setText(kargs.get('password', ''))
        self.form.cbPosition.setCurrentText(kargs.get('position', ''))
    
    def get_fields(self):
        return {
            'name' : self.form.cbName.currentText(),
            'username' : self.form.tbUserName.text(),
            'password' : self.form.tbPassword.text(),
            'confirm_password': self.form.tbConfirmPassword.text(),
            'position' : self.form.cbPosition.currentText()
        }
    
class BrowseUserForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Browse Users')
        self.setMinimumSize(600, 400)
        main_layout = QVBoxLayout(self)
        
        self.header = QLabel('Browse Users')
        self.form = UserForm()
        
        self.form.cbName.setDisabled(True)
        self.form.tbUserName.setReadOnly(True)
        self.form.tbPassword.setReadOnly(True)
        self.form.tbConfirmPassword.setReadOnly(True)
        self.form.cbPosition.setDisabled(True)
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
        
    def set_fields(self, **kargs):
        self.form.cbName.setCurrentText(kargs.get('name', ''))
        self.form.tbUserName.setText(kargs.get('username', ''))
        self.form.tbPassword.setText(kargs.get('password', ''))
        self.form.cbPosition.setCurrentText(kargs.get('position', ''))
    
class BlotterForm(QWidget):
    def __init__(self):
        super().__init__()
        
        main_layout = QFormLayout(self)
        
        self.tbRecordDate = QDateEdit()
        self.tbRecordDate.setCalendarPopup(True)
        self.cbStatus = QComboBox()
        self.cbStatus.addItems(['OPEN', 'ONGOING','CLOSED'])
        self.tbActionTaken = QLineEdit()
        self.tbNatureOfDispute = QLineEdit()
        self.tbComplainant = QLineEdit()
        self.tbRespondent = QLineEdit()
        self.tbFullReport = QTextEdit()
        
        main_layout.addRow('Record Date:', self.tbRecordDate)
        main_layout.addRow('Status:', self.cbStatus)
        main_layout.addRow('Action Taken:', self.tbActionTaken)
        main_layout.addRow('Nature of Dispute:', self.tbNatureOfDispute)
        main_layout.addRow('Complainant:', self.tbComplainant)
        main_layout.addRow('Respondent:', self.tbRespondent)
        main_layout.addRow('Full Report:', self.tbFullReport)
    
class AddBlotterForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Blotter')
        self.setMinimumSize(600, 400)
        main_layout = QVBoxLayout(self)
        
        self.header = QLabel('Add Blotter')
        self.form = BlotterForm()
        self.addbar = AddBar()
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
        main_layout.addWidget(self.addbar)
        
    def set_fields(self, **kargs):
        
        record_date = kargs.get('record_date', None)
        
        # If date_of_birth exists and is a date object, convert it to QDate
        if isinstance(record_date, date):
            # Extract year, month, and day from the date object
            qrecord_date = QDate(record_date.year, record_date.month, record_date.day)
        else:
            # Default to current date if no valid date is found
            qrecord_date = QDate.currentDate()
        
        self.form.tbRecordDate.setDate(qrecord_date)
        self.form.cbStatus.setCurrentText(kargs.get('status', ''))
        self.form.tbActionTaken.setText(kargs.get('action_taken', ''))
        self.form.tbNatureOfDispute.setText(kargs.get('nature_of_dispute', ''))
        self.form.tbComplainant.setText(kargs.get('complainant', ''))
        self.form.tbRespondent.setText(kargs.get('respondent', ''))
        self.form.tbFullReport.setText(kargs.get('full_report', ''))
        
    def get_fields(self):
        return {
            'record_date': self.form.tbRecordDate.date().toPython(),
            'status': self.form.cbStatus.currentText(),
            'action_taken': self.form.tbActionTaken.text(),
            'nature_of_dispute': self.form.tbNatureOfDispute.text(),
            'complainant': self.form.tbComplainant.text(),
            'respondent': self.form.tbRespondent.text(),
            'full_report': self.form.tbFullReport.toPlainText()
        }

class UpdateBlotterForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Update Blotter')
        self.setMinimumSize(600, 400)
        main_layout = QVBoxLayout(self)
        
        self.header = QLabel("Update Blotter")
        self.form = BlotterForm()
        self.updatebar = UpdateBar()
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
        main_layout.addWidget(self.updatebar)
        
    def set_fields(self, **kargs):
        
        record_date = kargs.get('record_date', None)
        
        # If date_of_birth exists and is a date object, convert it to QDate
        if isinstance(record_date, date):
            # Extract year, month, and day from the date object
            qrecord_date = QDate(record_date.year, record_date.month, record_date.day)
        else:
            # Default to current date if no valid date is found
            qrecord_date = QDate.currentDate()
        
        self.form.tbRecordDate.setDate(qrecord_date)
        self.form.cbStatus.setCurrentText(kargs.get('status', ''))
        self.form.tbActionTaken.setText(kargs.get('action_taken', ''))
        self.form.tbNatureOfDispute.setText(kargs.get('nature_of_dispute', ''))
        self.form.tbComplainant.setText(kargs.get('complainant', ''))
        self.form.tbRespondent.setText(kargs.get('respondent', ''))
        self.form.tbFullReport.setText(kargs.get('full_report', ''))
        
    def get_fields(self):
        return {
            'record_date': self.form.tbRecordDate.date().toPython(),
            'status': self.form.cbStatus.currentText(),
            'action_taken': self.form.tbActionTaken.text(),
            'nature_of_dispute': self.form.tbNatureOfDispute.text(),
            'complainant': self.form.tbComplainant.text(),
            'respondent': self.form.tbRespondent.text(),
            'full_report': self.form.tbFullReport.toPlainText()
        }
    
class BrowseBlotterForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Browse Blotter')
        self.setMinimumSize(600, 400)
        main_layout = QVBoxLayout(self)
        
        self.header = QLabel("Browse Blotter")
        self.form = BlotterForm()
        
        self.form.tbRecordDate.setReadOnly(True)
        self.form.cbStatus.setDisabled(True)
        self.form.tbActionTaken.setReadOnly(True)
        self.form.tbNatureOfDispute.setReadOnly(True)
        self.form.tbComplainant.setReadOnly(True)
        self.form.tbRespondent.setReadOnly(True)
        self.form.tbFullReport.setReadOnly(True)
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
        
    def set_fields(self, **kargs):
        
        record_date = kargs.get('record_date', None)
        
        # If date_of_birth exists and is a date object, convert it to QDate
        if isinstance(record_date, date):
            # Extract year, month, and day from the date object
            qrecord_date = QDate(record_date.year, record_date.month, record_date.day)
        else:
            # Default to current date if no valid date is found
            qrecord_date = QDate.currentDate()
        
        self.form.tbRecordDate.setDate(qrecord_date)
        self.form.cbStatus.setCurrentText(kargs.get('status', ''))
        self.form.tbActionTaken.setText(kargs.get('action_taken', ''))
        self.form.tbNatureOfDispute.setText(kargs.get('nature_of_dispute', ''))
        self.form.tbComplainant.setText(kargs.get('complainant', ''))
        self.form.tbRespondent.setText(kargs.get('respondent', ''))
        self.form.tbFullReport.setText(kargs.get('full_report', ''))

class CertificateForm(QWidget):
    def __init__(self):
        super().__init__()
        
        main_layout = QFormLayout(self)
        
        self.cbName = QComboBox()
        self.cbName.setEditable(True)
        completer = self.cbName.completer()
        completer.setFilterMode(Qt.MatchContains)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setCompletionMode(QCompleter.PopupCompletion) 
        self.cbName.setCompleter(completer)
        self.cbName.setInsertPolicy(QComboBox.NoInsert)
        
        self.tbDateIssued = QDateEdit()
        self.tbDateIssued.setCalendarPopup(True)
        self.cbType = QComboBox()
        self.cbType.addItems(['CLEARANCE', 'INDIGENCY', 'RESIDENCY'])
        self.tbPurpose = QTextEdit()
        
        main_layout.addRow('Name:', self.cbName)
        main_layout.addRow('Date Issued:', self.tbDateIssued)
        main_layout.addRow('Type:', self.cbType)
        main_layout.addRow('Purpose:', self.tbPurpose)

class AddCertificateForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Certificate')
        self.setMinimumSize(600, 400)
        main_layout = QVBoxLayout(self)
        
        self.header =  QLabel('Add Certificate')
        self.form = CertificateForm()
        self.addbar = AddBar()
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
        main_layout.addWidget(self.addbar)
    
    def set_fields(self, **kargs):
        self.form.cbName.addItems(kargs.get('name', ''))
        
    def get_fields(self):
        return {
            'name': self.form.cbName.currentText(),
            'date_issued': self.form.tbDateIssued.date().toPython(),
            'type': self.form.cbType.currentText(),
            'purpose': self.form.tbPurpose.toPlainText()
        }

class UpdateCertificateForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Update Certificate')
        self.setMinimumSize(600, 400)
        main_layout = QVBoxLayout(self)
        
        self.header =  QLabel('Update Certificate')
        self.form = CertificateForm()
        self.updatebar = UpdateBar()
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
        main_layout.addWidget(self.updatebar)
    
    def set_fields(self, **kargs):
        self.form.cbName.setCurrentText(kargs.get('name', ''))
        date_issued = kargs.get('date_issued', None)
        
        if isinstance(date_issued, date):
            qdate_issued = QDate(date_issued.year, date_issued.month, date_issued.day)
        else:
            qdate_issued = QDate.currentDate()
        
        self.form.tbDateIssued.setDate(qdate_issued)
        self.form.cbType.setCurrentText(kargs.get('type', ''))
        self.form.tbPurpose.setText(kargs.get('purpose', ''))
    
    def get_fields(self):
        return {
            'name': self.form.cbName.currentText(),
            'date_issued': self.form.tbDateIssued.date().toPython(),
            'type': self.form.cbType.currentText(),
            'purpose': self.form.tbPurpose.toPlainText()
        }

class BrowseCertificateForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Browse Certificate')
        self.setMinimumSize(600, 400)
        main_layout = QVBoxLayout(self)
        
        self.header = QLabel('Browse Certificate')
        self.form = CertificateForm()
        
        self.form.cbName.setDisabled(True)
        self.form.tbDateIssued.setReadOnly(True)
        self.form.cbType.setDisabled(True)
        self.form.tbPurpose.setReadOnly(True)

        self.tbPrint = QPushButton('Print')
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addWidget(self.tbPrint)
        main_layout.addStretch()
    
    def set_fields(self, **kargs):
        self.form.cbName.setCurrentText(kargs.get('name', ''))
        date_issued = kargs.get('date_issued', None)
        
        if isinstance(date_issued, date):
            qdate_issued = QDate(date_issued.year, date_issued.month, date_issued.day)
        else:
            qdate_issued = QDate.currentDate()
        
        self.form.tbDateIssued.setDate(qdate_issued)
        self.form.cbType.setCurrentText(kargs.get('type', ''))
        self.form.tbPurpose.setText(kargs.get('purpose', ''))



