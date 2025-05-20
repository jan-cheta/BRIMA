from PySide6.QtWidgets import (
    QApplication, QWizard, QWizardPage, QLineEdit, QLabel, QVBoxLayout, QMessageBox, QComboBox, QFormLayout, QGroupBox,
    QDateEdit
)
from sqlalchemy.orm import Session
from model import Barangay, Household, Resident, User 
import sys

class BarangayPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Enter Barangay Information")

        layout = QVBoxLayout()
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Barangay Name")
        layout.addWidget(QLabel("Barangay Name:"))
        layout.addWidget(self.name_edit)

        self.history_edit = QLineEdit()
        self.history_edit.setPlaceholderText("History")
        layout.addWidget(QLabel("History:"))
        layout.addWidget(self.history_edit)

        self.mission_edit = QLineEdit()
        self.mission_edit.setPlaceholderText("Mission")
        layout.addWidget(QLabel("Mission:"))
        layout.addWidget(self.mission_edit)

        self.vision_edit = QLineEdit()
        self.vision_edit.setPlaceholderText("Vision")
        layout.addWidget(QLabel("Vision:"))
        layout.addWidget(self.vision_edit)

        self.setLayout(layout)

    def validatePage(self):
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Input Error", "Barangay name cannot be empty.")
            return False
        return True


class HouseholdPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Enter Household Information")

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

    def validatePage(self):
        if not self.tbHouseholdName.text().strip():
            QMessageBox.warning(self, "Input Error", "Household name cannot be empty.")
            return False
        return True


class ResidentPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Enter Resident Information")

        layout = QVBoxLayout(self)  # Use QVBoxLayout for main layout

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

        layout.addWidget(personal_group)
        layout.addWidget(contact_group)
        layout.addWidget(other_group)

    def validatePage(self):
        if not self.tbFirstName.text().strip() or not self.tbLastName.text().strip():
            QMessageBox.warning(self, "Input Error", "First and last name cannot be empty.")
            return False
        if not self.tbCitizenship.text().strip():
            QMessageBox.warning(self, "Input Error", "Citizenship cannot be empty.")
            return False
        return True


class UserPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Create User Account")

        main_layout = QFormLayout(self)
        
        self.tbUserName = QLineEdit()
        self.tbPassword = QLineEdit()
        self.tbConfirmPassword = QLineEdit()
        self.tbPassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.tbConfirmPassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.cbPosition = QComboBox()
        self.cbPosition.addItems(["CAPTAIN", "SECRETARY", "TREASURER", "KAGAWAD", "TANOD"])
        
        main_layout.addRow('User Name:', self.tbUserName)
        main_layout.addRow('Password:', self.tbPassword)
        main_layout.addRow('Confirm Password', self.tbConfirmPassword)
        main_layout.addRow('Position:', self.cbPosition)

    def validatePage(self):
        if not self.tbUserName.text().strip() or not self.tbPassword.text().strip():
            QMessageBox.warning(self, "Input Error", "Username and password cannot be empty.")
            return False
        if not self.tbPassword.text().strip() == self.tbConfirmPassword.text().strip():
            QMessageBox.warning(self, "Input Error", "Passwords do not match.")
            return False
        return True


class InitWizard(QWizard):
    def __init__(self, session: Session):
        super().__init__()

        self.session = session

        self.barangay_page = BarangayPage()
        self.household_page = HouseholdPage()
        self.resident_page = ResidentPage()
        self.user_page = UserPage()

        self.addPage(self.barangay_page)
        self.addPage(self.household_page)
        self.addPage(self.resident_page)
        self.addPage(self.user_page)

        self.setWindowTitle("Application Initial Setup")

    def accept(self):
        # Gather all the data from pages
        barangay_name = self.barangay_page.name_edit.text().strip().upper()
        barangay_history = self.barangay_page.history_edit.text().strip().upper()
        barangay_mission = self.barangay_page.mission_edit.text().strip().upper()
        barangay_vision = self.barangay_page.vision_edit.text().strip().upper()

        household_name = self.household_page.tbHouseholdName.text().strip().upper()
        house_no = self.household_page.tbHouseNo.text().strip().upper()
        street = self.household_page.tbStreet.text().strip().upper()
        sitio = self.household_page.cbSitio.currentText().strip().upper()
        landmark = self.household_page.tbLandmark.text().strip().upper()

        # Resident fields (all upper except email)
        first_name = self.resident_page.tbFirstName.text().strip().upper()
        last_name = self.resident_page.tbLastName.text().strip().upper()
        middle_name = self.resident_page.tbMiddleName.text().strip().upper()
        suffix = self.resident_page.tbSuffix.text().strip().upper()
        dob = self.resident_page.tbBirthDate.date().toPython()
        phone1 = self.resident_page.tbPhone1.text().strip().upper()
        phone2 = self.resident_page.tbPhone2.text().strip().upper()
        email = self.resident_page.tbEmail.text().strip()  # emails are case-sensitive, do not upper
        occupation = self.resident_page.tbOccupation.text().strip().upper()
        civil_status = self.resident_page.cbCivilStatus.currentText().strip().upper()
        citizenship = self.resident_page.tbCitizenship.text().strip().upper()
        sex = self.resident_page.cbSex.currentText().strip().upper()
        education = self.resident_page.cbEducation.currentText().strip().upper()
        remarks = self.resident_page.tbRemarks.text().strip().upper()
        role = self.resident_page.cbRole.currentText().strip().upper()

        # User fields (username and password as is, position upper)
        username = self.user_page.tbUserName.text().strip()
        password = self.user_page.tbPassword.text().strip()
        position = self.user_page.cbPosition.currentText().strip().upper()

        # Save to DB
        barangay = Barangay(name=barangay_name, history=barangay_history, mission=barangay_mission, vision=barangay_vision)
        self.session.add(barangay)

        household = Household(household_name=household_name, house_no=house_no, street=street, sitio=sitio, landmark=landmark)
        self.session.add(household)

        resident = Resident(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            suffix=suffix,
            date_of_birth=dob,
            phone1=phone1,
            phone2=phone2,
            email=email,
            occupation=occupation,
            civil_status=civil_status,
            citizenship=citizenship,
            sex=sex,
            education=education,
            remarks=remarks,
            role=role,
            household=household
        )
        self.session.add(resident)

        user = User(
            username=username,
            password=password,
            position=position,
            resident=resident
        )
        self.session.add(user)

        self.session.commit()

        QMessageBox.information(self, "Setup Complete", "Initial data has been saved successfully. Restart Application and Login")
        super().accept()
