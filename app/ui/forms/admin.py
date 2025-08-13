from PySide6.QtWidgets import (
    QWidget, QFormLayout, QComboBox, QCompleter, QLineEdit
)

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
        
        self.header = FormHeader('Add User')
        self.form = UserForm()
        self.addbar = AddBar()
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
        main_layout.addWidget(self.addbar)
        
class UpdateUserForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Update User')
        self.setMinimumSize(600, 400)
        main_layout = QVBoxLayout(self)
        
        self.header = FormHeader('Update User')
        self.form = UserForm()
        self.updatebar = UpdateBar()
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
        main_layout.addWidget(self.updatebar)
    
class BrowseUserForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Browse Users')
        self.setMinimumSize(600, 400)
        main_layout = QVBoxLayout(self)
        
        self.header = FormHeader('Browse User')
        self.form = UserForm()
        
        self.form.cbName.setDisabled(True)
        self.form.tbUserName.setReadOnly(True)
        self.form.tbPassword.setReadOnly(True)
        self.form.tbConfirmPassword.setReadOnly(True)
        self.form.cbPosition.setDisabled(True)
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
    
class FilterUserForm(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Filter Users')
        main_layout = QVBoxLayout(self)

        self.header = FormHeader('Filter Users')
        self.form = QWidget()
        form_layout = QFormLayout(self.form)
        self.filterbar = FilterBar()
        self.cbPosition = QComboBox()
        self.cbPosition.addItems(['', 'CAPTAIN', 'SECRETARY', 'KAGAWAD', 'TANOD'])
        form_layout.addRow('Position: ', self.cbPosition)
                
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form)
        main_layout.addStretch()
        main_layout.addWidget(self.filterbar)