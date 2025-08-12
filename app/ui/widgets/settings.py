from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QGroupBox, QFormLayout,
    QHBoxLayout, QTextEdit, QLabel, QPushButtoni, QLineEdit, QPushButton
)

from PySide6.QtCore import Qt

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True) 
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        self.edit_barangay = QGroupBox()
        self.edit_barangay.setTitle('Edit Barangay Details')
        edit_barangay_layout = QVBoxLayout(self.edit_barangay)
        self.edit_barangay_form = QWidget()
        edit_barangay_form_layout = QFormLayout(self.edit_barangay_form)
        self.edit_barangay_buttons = QWidget()
        edit_barangay_buttons_layout = QHBoxLayout(self.edit_barangay_buttons)

        self.tbBarangayName = QLineEdit()
        self.tbHistory = QTextEdit()
        self.tbMission = QTextEdit()
        self.tbVision = QTextEdit()
        edit_barangay_form_layout.addRow('Barangay Name (Please Include Municipality/City): ', self.tbBarangayName)
        edit_barangay_form_layout.addRow('History: ', self.tbHistory)
        edit_barangay_form_layout.addRow('Mission: ', self.tbMission)
        edit_barangay_form_layout.addRow('Vision: ', self.tbVision)
        edit_barangay_layout.addWidget(self.edit_barangay_form)

        self.btSave = QPushButton('Save')
        self.btRevert = QPushButton('Revert')
        edit_barangay_buttons_layout.addStretch()
        edit_barangay_buttons_layout.addWidget(self.btRevert)
        edit_barangay_buttons_layout.addWidget(self.btSave)
        edit_barangay_layout.addWidget(self.edit_barangay_buttons)

        scroll_layout.addWidget(self.edit_barangay)

        self.export_csv = QGroupBox('Export')
        export_csv_layout = QVBoxLayout(self.export_csv)

        self.btExport = QPushButton('Export Data to XLSX')
        export_csv_layout.addWidget(self.btExport)

        scroll_layout.addWidget(self.export_csv)

        self.backup = QGroupBox('Data Backup')
        backup_layout = QVBoxLayout(self.backup)
        self.warning_label = QLabel(
            "WARNING: Use the backup function only when the current database is broken."
        )
        self.btCreateBackup = QPushButton('Create Backup')
        self.btViewBackup = QPushButton('Switch to Backup')
        backup_layout.addWidget(self.warning_label)
        backup_layout.addWidget(self.btCreateBackup)
        backup_layout.addWidget(self.btViewBackup)

        scroll_layout.addWidget(self.backup)

        scroll_area.setWidget(scroll_content)
        
        main_layout.addWidget(scroll_area)
