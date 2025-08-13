from PySide6.QtWidgets import (
    QWidget, QFormLayout, QComboBox, QCompleter, QDateEdit, QTextEdit,
    QDialog, QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import Qt
from ui.forms.components import FilterBar, FormHeader
from ui.forms.base import AddForm, UpdateForm, BrowseForm

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

class AddCertificateForm(AddForm):
    def __init__(self):
        super().__init__()
    
    def _set_header(self):
        return FormHeader("Add Certificate")
    
    def _set_form(self):
        return CertificateForm()

class UpdateCertificateForm(UpdateForm):
    def __init__(self):
        super().__init__()
    
    def _set_header(self):
        return FormHeader(" Certificate")
    
    def _set_form(self):
        return CertificateForm()

class BrowseCertificateForm(BrowseForm):
    def __init__(self):
        super().__init__()
    
    def _set_header(self):
        return FormHeader("Add Certificate")
    
    def _set_form(self):
        return CertificateForm()

class FilterCertificateForm(QDialog):
    def __init__(self):
        super().__init__()
     
        self.setWindowTitle('Filter Users')
        main_layout = QVBoxLayout(self)

        self.header = FormHeader('Filter Blotter')
        self.form = QWidget()
        form_layout = QFormLayout(self.form)
        self.filterbar = FilterBar()
        self.cbType = QComboBox()
        self.cbType.addItems(['CLEARANCE', 'INDIGENCY', 'RESIDENCY'])

        rd_widget = QWidget()
        rd_layout = QHBoxLayout()
        rd_widget.setLayout(rd_layout)
        
        self.tbStartRecordDate = QDateEdit()
        self.tbStartRecordDate.setCalendarPopup(True)
        self.tbEndRecordDate = QDateEdit()
        self.tbEndRecordDate.setCalendarPopup(True)

        rd_layout.addWidget(self.tbStartRecordDate)
        rd_layout.addWidget(self.tbEndRecordDate)

        form_layout.addRow('Status: ', self.cbType)
        form_layout.addRow('Record Date: ', rd_widget)
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
        main_layout.addWidget(self.filterbar)