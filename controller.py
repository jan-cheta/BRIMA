from base import Database
from model import Household, Resident, User, Blotter, Certificate, Barangay
from forms import (AddHouseholdForm, AddResidentForm, BrowseResidentForm,
    UpdateHouseholdForm, BrowseHouseholdForm, UpdateResidentForm, AddUserForm,
    UpdateUserForm, BrowseUserForm, AddBlotterForm, UpdateBlotterForm, BrowseBlotterForm,
    AddCertificateForm, UpdateCertificateForm, BrowseCertificateForm
)
from view import  BrimaView
from widgets import BaseWindow, AboutWindow, SettingsWindow
from PySide6.QtWidgets import QMessageBox, QDialog, QFileDialog
from PySide6.QtCore import Qt, QDate, QSize
from sqlalchemy import or_, and_, desc, select, create_engine
from sqlalchemy.orm import aliased, sessionmaker, declarative_base

import os
import shutil
from datetime import datetime
import pandas as pd


class MainController:
    def __init__(self, view : BrimaView):
        self.db = Database()
        self.session = self.db.get_session()
        self.view = view
        self.household_control = HouseholdWindowController(self.view.household_window)
        self.resident_control = ResidentWindowController(self.view.resident_window)
        self.user_control = UserWindowController(self.view.admin_window)
        self.blotter_control = BlotterWindowController(self.view.blotter_window)
        self.certificate_control = CertificateWindowController(self.view.certificate_window)
        self.about_control = AboutUsWindowController(self.view.about_window)
        self.settings_control = SettingsWindowControl(self.view.settings_window)

        self.view.btHousehold.clicked.connect(lambda: self.view.stack.setCurrentIndex(0))
        self.view.btResident.clicked.connect(lambda: self.view.stack.setCurrentIndex(1))
        self.view.btAdmin.clicked.connect(lambda: self.view.stack.setCurrentIndex(2))
        self.view.btBlotter.clicked.connect(lambda: self.view.stack.setCurrentIndex(3))
        self.view.btCertificate.clicked.connect(lambda: self.view.stack.setCurrentIndex(4))
        self.view.btAboutUs.clicked.connect(lambda: self.view.stack.setCurrentIndex(5))
        self.view.btAboutUs.clicked.connect(self.about_control.load_data)
        self.view.btSettings.clicked.connect(lambda: self.view.stack.setCurrentIndex(6))


class HouseholdWindowController:
    def __init__(self, view: BaseWindow):
        self.db = Database()
        self.session = self.db.get_session()
        self.view = view
        self.refresh()
        
        self.view.btRefresh.clicked.connect(self.refresh)
        self.view.btSearch.clicked.connect(self.search)
        self.view.tbSearchBar.returnPressed.connect(self.search)
        self.view.btAdd.clicked.connect(self.add)
        self.view.btEdit.clicked.connect(self.edit)
        self.view.btDelete.clicked.connect(self.delete)
        self.view.btBrowse.clicked.connect(self.browse)
        
    def refresh(self):
        self.view.set_search_text('')
        households = self.session.query(Household).order_by(Household.household_name).all()
        data = []
        for household in households:
            result = [
                household.id,
                household.household_name,
                f"{household.house_no} {household.street} {household.sitio} {household.landmark}"
            ]
            data.append(result)
        
        self.view.load_table(['id', 'Household Name', 'Address'], data)
    
    def search(self):
        search_text = self.view.get_search_text().lower()  
        search_terms = search_text.split() 
        
        # Base query
        query = self.session.query(Household)
        
        # Apply AND of ORs: each term must match one of the fields
        if search_terms:
            conditions = []
            for term in search_terms:
                term_filter = or_(
                    Household.household_name.ilike(f"%{term}%"),
                    Household.house_no.ilike(f"%{term}%"),
                    Household.street.ilike(f"%{term}%"),
                    Household.sitio.ilike(f"%{term}%"),
                    Household.landmark.ilike(f"%{term}%")
                )
                conditions.append(term_filter)
            
            query = query.filter(and_(*conditions))
        
        # Order and execute
        households = query.order_by(Household.household_name).all()
        
        data = []
        for household in households:
            address = " ".join(filter(None, [
                household.house_no,
                household.street,
                household.sitio,
                household.landmark
            ]))
            
            result = [
                household.id,
                household.household_name,
                address
            ]
            data.append(result)
        
        self.view.load_table(['id', 'Household Name', 'Address'], data)
    
    def add(self):
            add_form = AddHouseholdForm()
            add_form.addbar.btAdd.clicked.connect(add_form.accept)
            add_form.addbar.btCancel.clicked.connect(add_form.reject)
            
            # Execute the form as a modal dialog
            if add_form.exec() == QDialog.Accepted:
                # Get the data from the form
                data = add_form.get_fields()
                data = {key: value.upper() if isinstance(value, str) else value for key, value in data.items()}
                
                new_household = Household(**data)
                
                try:
                    self.session.add(new_household)
                    self.session.commit()
                    QMessageBox.information(add_form, "Success", "Household added successfully!")
                    
                    self.refresh()
                except Exception as e:
                    self.session.rollback()
                    QMessageBox.critical(self.view, "Error", f"Failed to add household: {str(e)}")

    
    def edit(self):
        row_id = self.view.get_table_row()
        if row_id:
            household = self.session.query(Household).get(row_id)
            
            if household:
                update_form = UpdateHouseholdForm()
                
                update_form.set_fields(
                    household_name=household.household_name,
                    house_no=household.house_no,
                    street=household.street,
                    sitio=household.sitio,
                    landmark=household.landmark
                )
                
                update_form.updatebar.btRevert.clicked.connect(
                    lambda: update_form.set_fields(
                        household_name=household.household_name,
                        house_no=household.house_no,
                        street=household.street,
                        sitio=household.sitio,
                        landmark=household.landmark
                    )
                )
                
                update_form.updatebar.btUpdate.clicked.connect(
                    lambda: self.save_update(household, update_form)
                )
                
                update_form.updatebar.btCancel.clicked.connect(update_form.reject)
                
                if update_form.exec() == QDialog.Accepted:
                    self.refresh()
    
    def save_update(self, household, update_form):
        data = update_form.get_fields()
        data = {key: value.upper() if isinstance(value, str) else value for key, value in data.items()}
        
        household.household_name = data['household_name']
        household.house_no = data['house_no']
        household.street = data['street']
        household.sitio = data['sitio']
        household.landmark = data['landmark']
        
        try:
            self.session.commit()
            QMessageBox.information(self.view, "Success", "Household updated successfully!")
        except Exception as e:
            self.session.rollback()  
            QMessageBox.critical(self.view, "Error", f"Failed to update household: {str(e)}")
        
        update_form.accept()   
        
    def browse(self):
        row_id = self.view.get_table_row()
        if row_id:
            household = self.session.query(Household).get(row_id)
            
            if household:
                browse_form = BrowseHouseholdForm()
                
                browse_form.set_fields(
                    household_name=household.household_name,
                    house_no=household.house_no,
                    street=household.street,
                    sitio=household.sitio,
                    landmark=household.landmark
                )
                
                browse_form.exec()
        
    
    def delete(self):
        row_id = self.view.get_table_row()
        if row_id:
            household = self.session.query(Household).get(row_id)
            if household:
                reply = QMessageBox.question(
                    self.view,  # Parent widget
                    "Confirm Deletion",
                    f"Are you sure you want to delete '{household.household_name}'?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
    
                if reply == QMessageBox.Yes:
                    self.session.delete(household)
                    self.session.commit()
                    self.refresh()

class ResidentWindowController:
    def __init__(self, view: BaseWindow):
        self.db = Database()
        self.session = self.db.get_session()
        self.view = view
        self.refresh()
        
        self.view.btRefresh.clicked.connect(self.refresh)
        self.view.btSearch.clicked.connect(self.search)
        self.view.tbSearchBar.returnPressed.connect(self.search)
        self.view.btAdd.clicked.connect(self.add)
        self.view.btEdit.clicked.connect(self.edit)
        self.view.btDelete.clicked.connect(self.delete)
        self.view.btBrowse.clicked.connect(self.browse)
        
    def refresh(self):
        self.view.set_search_text('')
        residents = self.session.query(Resident).order_by(Resident.last_name, Resident.household_id).all()
        data = []
        for resident in residents:
            full_name = " ".join(filter(None, [resident.first_name, resident.middle_name, resident.suffix]))
            full_name = f"{resident.last_name}, {full_name}".strip()
    
            household = resident.household
            household_name = household.household_name if household else "N/A"
            address_parts = [
                getattr(household, "house_no", ""),
                getattr(household, "street", ""),
                getattr(household, "sitio", ""),
                getattr(household, "landmark", "")
            ] if household else []
    
            address = " ".join(filter(None, address_parts))
    
            result = [
                resident.id,
                full_name,
                resident.role,
                household_name,
                address
            ]
            data.append(result)
        
        self.view.load_table(['id', 'Full Name', 'Role', 'Household Name', 'Address'], data)
    
    def search(self):
        search_text = self.view.get_search_text().lower()
        search_terms = search_text.split()
    
        # Start with base query and join household
        query = self.session.query(Resident).join(Resident.household)
    
        # Apply search filters
        if search_terms:
            conditions = []
            for term in search_terms:
                term_filter = or_(
                    Resident.first_name.ilike(f"%{term}%"),
                    Resident.middle_name.ilike(f"%{term}%"),
                    Resident.last_name.ilike(f"%{term}%"),
                    Resident.suffix.ilike(f"%{term}%"),
                    Resident.role.ilike(f"%{term}%"),
                    Household.household_name.ilike(f"%{term}%"),
                    Household.house_no.ilike(f"%{term}%"),
                    Household.street.ilike(f"%{term}%"),
                    Household.sitio.ilike(f"%{term}%"),
                    Household.landmark.ilike(f"%{term}%")
                )
                conditions.append(term_filter)
            
            query = query.filter(and_(*conditions))
    
        # Apply sorting
        residents = query.order_by(Resident.last_name, Resident.household_id).all()
    
        # Format results
        data = []
        for resident in residents:
            full_name = " ".join(filter(None, [
                resident.first_name,
                resident.middle_name,
                resident.suffix
            ]))
            full_name = f"{resident.last_name}, {full_name}".strip()
    
            household = resident.household
            household_name = household.household_name if household else "N/A"
            address_parts = [
                getattr(household, "house_no", ""),
                getattr(household, "street", ""),
                getattr(household, "sitio", ""),
                getattr(household, "landmark", "")
            ] if household else []
    
            address = " ".join(filter(None, address_parts))
    
            result = [
                resident.id,
                full_name,
                resident.role,
                household_name,
                address
            ]
            data.append(result)
    
        # Load into the view
        self.view.load_table(['id', 'Full Name', 'Role', 'Household Name', 'Address'], data)
    
    def add(self):
        add_form = AddResidentForm()
    
        # Populate households for dropdown (household names and IDs)
        households = self.session.query(Household).order_by(Household.household_name).all()
        household_dict = {household.household_name: household.id for household in households}
    
        # Set the fields for the form (populate the household dropdown with names)
        add_form.set_fields(household=list(household_dict.keys()))
        add_form.form.cbHousehold.setCurrentText('')  # Ensure no default value is set
        add_form.form.cbHousehold.currentTextChanged.connect(lambda: self.autofill_household(household_dict, add_form))
    
        # Button signals
        add_form.addbar.btAdd.clicked.connect(lambda: self.on_add_button_click(add_form, household_dict))
        add_form.addbar.btCancel.clicked.connect(add_form.reject)
    
        # Execute the form as a modal dialog
        add_form.exec()
    
    def on_add_button_click(self, add_form, household_dict):
        # Get the data from the form
        data = add_form.get_fields()
    
        # Check if 'household' is present and valid in the data
        household_name = data.get("household")  # Use get to avoid KeyError
        if not household_name:  # Check if the household field is empty
            QMessageBox.critical(add_form, "Error", "Please select a Household.")
            return  # Exit if the household is not selected or invalid
        
        # Retrieve the corresponding Household ID from the dictionary
        household_id = household_dict.get(household_name)
        if not household_id:
            QMessageBox.critical(add_form, "Error", f"No matching Household found for '{household_name}'.")
            return  # Exit if no valid household ID is found
        
        # Get the Household object from the database using the household ID
        household = self.session.query(Household).get(household_id)
    
        # Remove the 'household' key from the data dictionary since it's already handled
        del data['household']
    
        # Uppercase all string values in data (excluding non-string types)
        data = {key: value.upper() if isinstance(value, str) else value for key, value in data.items()}
    
        # Create a new Resident instance with the provided data
        new_resident = Resident(**data)
        new_resident.household = household  # Associate the resident with the selected household
    
        try:
            # Add the new resident to the session and commit the transaction
            self.session.add(new_resident)
            self.session.commit()
            QMessageBox.information(add_form, "Success", "Resident added successfully!")
            self.refresh()  # Refresh the view/list of residents
            
            # Close the dialog only if everything is successful
            add_form.accept()
        except Exception as e:
            # If any error occurs, roll back the session and display an error message
            self.session.rollback()
            QMessageBox.critical(add_form, "Error", f"Failed to add resident: {str(e)}")
            add_form.activateWindow()  # Ensure focus returns to the dialog
            add_form.raise_()
    
    def autofill_household(self, data, view):
        id = data[view.form.cbHousehold.currentText()]
        
        if id:
            household = self.session.query(Household).get(id)
            
            view.form.tbHouseholdName.setText(household.household_name)
            view.form.tbHouseNo.setText(household.house_no)
            view.form.tbStreet.setText(household.street)
            view.form.cbSitio.setCurrentText(household.sitio)
            view.form.tbLandmark.setText(household.landmark)
        
    
    def edit(self):
        row_id = self.view.get_table_row()
        if row_id:
            resident = self.session.query(Resident).get(row_id)
    
            if resident:
                update_form = UpdateResidentForm()
    
                # Fetch households
                households = self.session.query(Household).order_by(Household.household_name).all()
                household_dict = {household.household_name: household.id for household in households}
                household_names = list(household_dict.keys())
    
                # Populate household combo box
                update_form.form.cbHousehold.clear()
                update_form.form.cbHousehold.addItems(household_names)
                update_form.form.cbHousehold.setCurrentText(resident.household.household_name if resident.household else '')
                self.autofill_household(household_dict, update_form)
    
                update_form.form.cbHousehold.currentTextChanged.connect(
                    lambda: self.autofill_household(household_dict, update_form)
                )
    
                # Set initial values
                update_form.set_fields(
                    first_name=resident.first_name,
                    last_name=resident.last_name,
                    middle_name=resident.middle_name,
                    suffix=resident.suffix,
                    date_of_birth=resident.date_of_birth,
                    phone1=resident.phone1,
                    phone2=resident.phone2,
                    email=resident.email,
                    household=resident.household.household_name if resident.household else '',
                    occupation=resident.occupation,
                    civil_status=resident.civil_status,
                    education=resident.education,
                    remarks=resident.remarks,
                    sex=resident.sex,
                    role=resident.role,
                )
    
                # Revert button restores original values
                update_form.updatebar.btRevert.clicked.connect(
                    lambda: update_form.set_fields(
                        first_name=resident.first_name,
                        last_name=resident.last_name,
                        middle_name=resident.middle_name,
                        suffix=resident.suffix,
                        date_of_birth=resident.date_of_birth,
                        phone1=resident.phone1,
                        phone2=resident.phone2,
                        email=resident.email,
                        household=resident.household.household_name if resident.household else '',
                        occupation=resident.occupation,
                        civil_status=resident.civil_status,
                        education=resident.education,
                        remarks=resident.remarks,
                        sex=resident.sex,
                        role=resident.role,
                    )
                )
    
                # Save button
                update_form.updatebar.btUpdate.clicked.connect(
                    lambda: self.save_update(resident, update_form, household_dict)
                )
    
                # Cancel button
                update_form.updatebar.btCancel.clicked.connect(update_form.reject)
    
                update_form.exec()
    
    
    def save_update(self, resident, update_form, household_dict):
        updated_data = update_form.get_fields()
    
        # Map household name to ID
        household_name = update_form.form.cbHousehold.currentText()
        household_id = household_dict.get(household_name)
    
        if not household_id:
            QMessageBox.critical(update_form, "Error", "Please select a valid household.")
            return
    
        household = self.session.query(Household).get(household_id)
        if not household:
            QMessageBox.critical(update_form, "Error", "Selected household does not exist.")
            return
    
        # Update resident fields
        resident.first_name = updated_data["first_name"].upper()
        resident.last_name = updated_data["last_name"].upper()
        resident.middle_name = updated_data["middle_name"].upper()
        resident.suffix = updated_data["suffix"].upper()
        resident.date_of_birth = updated_data["date_of_birth"]
        resident.phone1 = updated_data["phone1"]
        resident.phone2 = updated_data["phone2"]
        resident.email = updated_data["email"]
        resident.occupation = updated_data["occupation"]
        resident.civil_status = updated_data["civil_status"]
        resident.education = updated_data["education"]
        resident.remarks = updated_data["remarks"]
        resident.sex = updated_data["sex"]
        resident.role = updated_data["role"]
        resident.household = household
    
        try:
            self.session.commit()
            QMessageBox.information(update_form, "Success", "Resident updated successfully!")
            update_form.accept()
            self.refresh()
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(update_form, "Error", f"Failed to update resident: {str(e)}")
        
    def browse(self):
        row_id = self.view.get_table_row()
        if row_id:
            resident = self.session.query(Resident).get(row_id)
            
            if resident:
                browse_form = BrowseResidentForm()
                
                browse_form.set_fields(
                    first_name=resident.first_name,
                    last_name=resident.last_name,
                    middle_name=resident.middle_name,
                    suffix=resident.suffix,
                    date_of_birth=resident.date_of_birth,
                    phone1=resident.phone1,
                    phone2=resident.phone2,
                    email=resident.email,
                    household=resident.household.household_name if resident.household else '',
                    occupation=resident.occupation,
                    civil_status=resident.civil_status,
                    education=resident.education,
                    remarks=resident.remarks,
                    sex=resident.sex,
                    role=resident.role,
                )
                
                households = self.session.query(Household).order_by(Household.household_name).all()
                household_dict = {household.household_name: household.id for household in households}
                household_names = list(household_dict.keys())
    
                # Populate household combo box
                browse_form.form.cbHousehold.setCurrentText(resident.household.household_name if resident.household else '')
                self.autofill_household(household_dict, browse_form)
                
                browse_form.exec()
        
    
    def delete(self):
        row_id = self.view.get_table_row()
        if row_id:
            resident = self.session.query(Resident).get(row_id)
            if resident:
                reply = QMessageBox.question(
                    self.view, 
                    "Confirm Deletion",
                    f"Are you sure you want to delete {resident.last_name}, {resident.first_name} {resident.middle_name} {resident.suffix}?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
    
                if reply == QMessageBox.Yes:
                    self.session.delete(resident)
                    self.session.commit()
                    self.refresh()

class UserWindowController:
    def __init__(self, view: BaseWindow):
        self.db = Database()
        self.session = self.db.get_session()
        self.view = view
        self.refresh()
        
        self.view.btRefresh.clicked.connect(self.refresh)
        self.view.btSearch.clicked.connect(self.search)
        self.view.tbSearchBar.returnPressed.connect(self.search)
        self.view.btAdd.clicked.connect(self.add)
        self.view.btEdit.clicked.connect(self.edit)
        self.view.btDelete.clicked.connect(self.delete)
        self.view.btBrowse.clicked.connect(self.browse)
    
    def refresh(self):
        self.view.set_search_text('')
        users = self.session.query(User).join(User.resident).order_by(User.position, Resident.last_name).all()
        data = []
        for user in users:
            
            username = user.username
            position = user.position
            resident = user.resident
            resident_name = [
                getattr(resident, "first_name", ""),
                getattr(resident, "middle_name", ""),
                getattr(resident, "last_name", ""),
                getattr(resident, "suffix", "")
            ] if resident else []
    
            full_name = " ".join(filter(None, resident_name))
    
            result = [
                user.id,
                username,
                position,
                full_name,
            ]
            data.append(result)
        
        self.view.load_table(['id', 'Username', 'Position', 'Full Name'], data)
        
    def search(self):
        search_text = self.view.get_search_text().lower()
        search_terms = search_text.split()
    
        # Start with base query and join household
        query = self.session.query(User).join(User.resident)
    
        # Apply search filters
        if search_terms:
            conditions = []
            for term in search_terms:
                term_filter = or_(
                    Resident.first_name.ilike(f"%{term}%"),
                    Resident.middle_name.ilike(f"%{term}%"),
                    Resident.last_name.ilike(f"%{term}%"),
                    Resident.suffix.ilike(f"%{term}%"),
                    User.username.ilike(f"%{term}%"),
                    User.position.ilike(f"%{term}%"),
                )
                conditions.append(term_filter)
            
            query = query.filter(and_(*conditions))
    
        # Apply sorting
        users = query.order_by(User.position, Resident.last_name).all()
    
        # Format results
        data = []
        for user in users:
            
            username = user.username
            position = user.position
            resident = user.resident
            resident_name = [
                getattr(resident, "first_name", ""),
                getattr(resident, "middle_name", ""),
                getattr(resident, "last_name", ""),
                getattr(resident, "suffix", "")
            ] if resident else []
    
            full_name = " ".join(filter(None, resident_name))
    
            result = [
                user.id,
                username,
                position,
                full_name,
            ]
            data.append(result)
        
        self.view.load_table(['id', 'Username', 'Position', 'Full Name'], data)
    
    def add(self):
        add_form = AddUserForm()
    
        # Populate households for dropdown (household names and IDs)
        residents = self.session.query(Resident).filter(Resident.user == None).order_by(Resident.last_name).all()
        resident_dict = {
            " ".join(filter(None, [
                resident.first_name,
                resident.middle_name,
                resident.last_name,
                resident.suffix
            ])): resident.id
            for resident in residents
        }
    
        # Set the fields for the form (populate the household dropdown with names)
        add_form.set_fields(name=list(resident_dict.keys()))
        add_form.form.cbName.setCurrentText('')  # Ensure no default value is set
    
        # Button signals
        add_form.addbar.btAdd.clicked.connect(lambda: self.on_add_button_click(add_form, resident_dict))
        add_form.addbar.btCancel.clicked.connect(add_form.reject)
    
        # Execute the form as a modal dialog
        add_form.exec()
    
    def on_add_button_click(self, add_form, resident_dict):
        data = add_form.get_fields()
    
        resident_name = data.get("name")
        if not resident_name:  
            QMessageBox.critical(add_form, "Error", "Please select a Resident.")
            return  
        
        resident_id = resident_dict.get(resident_name)
        if not resident_id:
            QMessageBox.critical(add_form, "Error", f"No matching Household found for '{resident_name}'.")
            return  
            
        resident = self.session.query(Resident).get(resident_id)
    
        # Remove the 'household' key from the data dictionary since it's already handled
        del data['name']
    
        # Uppercase all string values in data (excluding non-string types)
        data = {key: value.upper() if isinstance(value, str) and key != 'username' and key != 'password' else value for key, value in data.items()}
    
        # Create a new Resident instance with the provided data
        new_user = User(**data)
        new_user.resident = resident  # Associate the resident with the selected household
    
        try:
            # Add the new resident to the session and commit the transaction
            self.session.add(new_user)
            self.session.commit()
            QMessageBox.information(add_form, "Success", "User added successfully!")
            self.refresh()  
            
            # Close the dialog only if everything is successful
            add_form.accept()
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(add_form, "Error", f"Failed to add resident: {str(e)}")
            add_form.activateWindow() 
            add_form.raise_()    
    
    def edit(self):
        row_id = self.view.get_table_row()
        if row_id:
            user = self.session.query(User).get(row_id)
    
            if user:
                update_form = UpdateUserForm()
    
                # Fetch households
                residents = self.session.query(Resident).filter(Resident.user == None).order_by(Resident.last_name).all()
                resident_dict = {
                    " ".join(filter(None, [
                        resident.first_name,
                        resident.middle_name,
                        resident.last_name,
                        resident.suffix
                    ])): resident.id
                    for resident in residents
                }
                resident_names = list(resident_dict.keys())
    
                # Populate household combo box
                update_form.form.cbName.clear()
                update_form.form.cbName.addItems(resident_names)
                full_name = ""
                if user.resident:
                    full_name = " ".join(filter(None, [
                        user.resident.first_name,
                        user.resident.middle_name,
                        user.resident.last_name,
                        user.resident.suffix
                    ]))
                    update_form.form.cbName.setCurrentText(full_name)
    
    
                # Set initial values
                update_form.set_fields(
                    name = full_name,
                    username = user.username,
                    password = user.password,
                    position = user.position
                )
    
                # Revert button restores original values
                update_form.updatebar.btRevert.clicked.connect(
                    lambda: update_form.set_fields(
                        name = full_name,
                        username = user.username,
                        password = user.password,
                        position = user.position
                    )
                )
    
                # Save button
                update_form.updatebar.btUpdate.clicked.connect(
                    lambda: self.save_update(user, update_form, resident_dict)
                )
    
                # Cancel button
                update_form.updatebar.btCancel.clicked.connect(update_form.reject)
    
                update_form.exec()
    
    
    def save_update(self, user, update_form, resident_dict):
        updated_data = update_form.get_fields()
    
        # Map household name to ID
        resident_name = update_form.form.cbName.currentText()
        resident_id = resident_dict.get(resident_name)
    
        if not resident_name:
            QMessageBox.critical(update_form, "Error", "Please select a valid resident.")
            return
    
        resident = self.session.query(Resident).get(resident_id)
        if not resident:
            QMessageBox.critical(update_form, "Error", "Selected resident does not exist.")
            return
    
        # Update resident fields
        user.username = updated_data['username']
        user.password = updated_data['password']
        user.position = updated_data['position']
        user.resident = resident
    
        try:
            self.session.commit()
            QMessageBox.information(update_form, "Success", "User updated successfully!")
            update_form.accept()
            self.refresh()
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(update_form, "Error", f"Failed to update User: {str(e)}")
        
    def browse(self):
        row_id = self.view.get_table_row()
        if row_id:
            user = self.session.query(User).get(row_id)
            
            if user:
                browse_form = BrowseUserForm()
                resident = user.resident
                
                full_name = " ".join(filter(None, [
                    resident.first_name,
                    resident.middle_name,
                    resident.last_name,
                    resident.suffix
                ]))
                browse_form.set_fields(
                    name = full_name,
                    username = user.username,
                    password = user.password,
                    position = user.position
                   
                )
                
                browse_form.exec()
    
    def delete(self):
        row_id = self.view.get_table_row()
        if row_id:
            user = self.session.query(User).get(row_id)
            if user:
                reply = QMessageBox.question(
                    self.view, 
                    "Confirm Deletion",
                    f"Are you sure you want to delete User: {user.username}?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
    
                if reply == QMessageBox.Yes:
                    self.session.delete(user)
                    self.session.commit()
                    self.refresh()

class BlotterWindowController:
    def __init__(self, view : BaseWindow):
        self.db = Database()
        self.session = self.db.get_session()
        self.view = view
        self.refresh()
        
        self.view.btRefresh.clicked.connect(self.refresh)
        self.view.btSearch.clicked.connect(self.search)
        self.view.tbSearchBar.returnPressed.connect(self.search)
        self.view.btAdd.clicked.connect(self.add)
        self.view.btEdit.clicked.connect(self.edit)
        self.view.btDelete.clicked.connect(self.delete)
        self.view.btBrowse.clicked.connect(self.browse)
    
    def refresh(self):
        self.view.set_search_text('')
        blotters = self.session.query(Blotter).order_by(desc(Blotter.record_date)).all()
        data = []
        for blotter in blotters:
            result = [
                blotter.id,
                blotter.record_date,
                blotter.complainant,
                blotter.respondent,
                blotter.status,
                str(blotter.full_report)[:20]
            ]
            data.append(result)
        
        self.view.load_table(['id', 'Record Date', 'Complainant', 'Respondent', 'Status','Report'], data)
    
    def search(self):
        search_text = self.view.get_search_text().lower()  
        search_terms = search_text.split() 
        
        # Base query
        query = self.session.query(Blotter)
        
        # Apply AND of ORs: each term must match one of the fields
        if search_terms:
            conditions = []
            for term in search_terms:
                term_filter = or_(
                    Blotter.record_date.ilike(f"%{term}%"),
                    Blotter.complainant.ilike(f"%{term}%"),
                    Blotter.respondent.ilike(f"%{term}%"),
                    Blotter.status.ilike(f"%{term}%"),
                    Blotter.full_report.ilike(f"%{term}%"),
                )
                conditions.append(term_filter)
            
            query = query.filter(and_(*conditions))
        
        # Order and execute
        blotters = query.order_by(desc(Blotter.record_date)).all()
        
        data = []
        for blotter in blotters:
            result = [
                blotter.id,
                blotter.record_date,
                blotter.complainant,
                blotter.respondent,
                blotter.status,
                str(blotter.full_report)[:20]
            ]
            data.append(result)
        
        self.view.load_table(['id', 'Record Date', 'Complainant', 'Respondent', 'Status','Report'], data)
    
    def add(self):
            add_form = AddBlotterForm()
            add_form.addbar.btAdd.clicked.connect(add_form.accept)
            add_form.addbar.btCancel.clicked.connect(add_form.reject)
            add_form.form.tbRecordDate.setDate(QDate.currentDate())
            
            # Execute the form as a modal dialog
            if add_form.exec() == QDialog.Accepted:
                # Get the data from the form
                data = add_form.get_fields()
                data = {key: value.upper() if isinstance(value, str) else value for key, value in data.items()}
                
                new_blotter = Blotter(**data)
                
                try:
                    self.session.add(new_blotter)
                    self.session.commit()
                    QMessageBox.information(add_form, "Success", "Blotter added successfully!")
                    
                    self.refresh()
                except Exception as e:
                    self.session.rollback()
                    QMessageBox.critical(self.view, "Error", f"Failed to add blotter: {str(e)}")

    
    def edit(self):
        row_id = self.view.get_table_row()
        if row_id:
            blotter = self.session.query(Blotter).get(row_id)
            
            if blotter:
                update_form = UpdateBlotterForm()
                
                update_form.set_fields(
                    record_date = blotter.record_date,
                    status = blotter.status,
                    action_taken = blotter.action_taken,
                    nature_of_dispute = blotter.nature_of_dispute,
                    complainant = blotter.complainant,
                    respondent = blotter.respondent,
                    full_report = blotter.full_report
                )
                
                update_form.updatebar.btRevert.clicked.connect(
                    lambda: update_form.set_fields(
                        record_date = blotter.record_date,
                        status = blotter.statis,
                        action_taken = blotter.action_taken,
                        nature_of_dispute = blotter.nature_of_dispute,
                        complainant = blotter.complainant,
                        respondent = blotter.respondent,
                        full_report = blotter.full_report
                    )
                )
                
                update_form.updatebar.btUpdate.clicked.connect(
                    lambda: self.save_update(blotter, update_form)
                )
                
                update_form.updatebar.btCancel.clicked.connect(update_form.reject)
                
                if update_form.exec() == QDialog.Accepted:
                    self.refresh()
    
    def save_update(self, blotter, update_form):
        data = update_form.get_fields()
        data = {key: value.upper() if isinstance(value, str) else value for key, value in data.items()}
        
        blotter.record_date = data['record_date']
        blotter.status = data['status']
        blotter.action_taken = data['action_taken']
        blotter.nature_of_dispute = data['nature_of_dispute']
        blotter.complainant = data['complainant']
        blotter.respondent = data['respondent']
        blotter.full_report = data['full_report']
        
        try:
            self.session.commit()
            QMessageBox.information(self.view, "Success", "Blotter updated successfully!")
        except Exception as e:
            self.session.rollback()  
            QMessageBox.critical(self.view, "Error", f"Failed to update blotter: {str(e)}")
        
        update_form.accept()   
        
    def browse(self):
        row_id = self.view.get_table_row()
        if row_id:
            blotter = self.session.query(Blotter).get(row_id)
            
            if blotter:
                browse_form = BrowseBlotterForm()
                
                browse_form.set_fields(
                    record_date = blotter.record_date,
                    status = blotter.status,
                    action_taken = blotter.action_taken,
                    nature_of_dispute = blotter.nature_of_dispute,
                    complainant = blotter.complainant,
                    respondent = blotter.respondent,
                    full_report = blotter.full_report
                )
                
                browse_form.exec()
        
    
    def delete(self):
        row_id = self.view.get_table_row()
        if row_id:
            blotter = self.session.query(Blotter).get(row_id)
            if blotter:
                reply = QMessageBox.question(
                    self.view,  # Parent widget
                    "Confirm Deletion",
                    f"Are you sure you want to delete '{str(blotter.full_text)[:20]}'?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
    
                if reply == QMessageBox.Yes:
                    self.session.delete(blotter)
                    self.session.commit()
                    self.refresh()
                    
class CertificateWindowController:
    def __init__(self, view: BaseWindow):
        self.db = Database()
        self.session = self.db.get_session()
        self.view = view
        self.refresh()
        
        self.view.btRefresh.clicked.connect(self.refresh)
        self.view.btSearch.clicked.connect(self.search)
        self.view.tbSearchBar.returnPressed.connect(self.search)
        self.view.btAdd.clicked.connect(self.add)
        self.view.btEdit.clicked.connect(self.edit)
        self.view.btDelete.clicked.connect(self.delete)
        self.view.btBrowse.clicked.connect(self.browse)
    
    def refresh(self):
        self.view.set_search_text('')
        certificates = self.session.query(Certificate).join(Certificate.resident).order_by(desc(Certificate.date_issued)).all()
        data = []
        for certificate in certificates:
            resident = certificate.resident 
            date_issued = certificate.date_issued
            type = certificate.type
            purpose = certificate.purpose
            resident_name = [
                getattr(resident, "first_name", ""),
                getattr(resident, "middle_name", ""),
                getattr(resident, "last_name", ""),
                getattr(resident, "suffix", "")
            ] if resident else []
    
            full_name = " ".join(filter(None, resident_name))
    
            result = [
                certificate.id,
                date_issued,
                type,
                full_name,
                purpose
            ]
            data.append(result)
        
        self.view.load_table(['id', 'Date Issued', 'Type', 'Resident', 'Purpose'], data)
        
    def search(self):
        search_text = self.view.get_search_text().lower()
        search_terms = search_text.split()
    
        # Start with base query and join household
        query = self.session.query(Certificate).join(Certificate.resident)
    
        # Apply search filters
        if search_terms:
            conditions = []
            for term in search_terms:
                term_filter = or_(
                    Resident.first_name.ilike(f"%{term}%"),
                    Resident.middle_name.ilike(f"%{term}%"),
                    Resident.last_name.ilike(f"%{term}%"),
                    Resident.suffix.ilike(f"%{term}%"),
                    Certificate.date_issued.ilike(f"%{term}%"),
                    Certificate.type.ilike(f"%{term}%"),
                    Certificate.purpose.ilike(f"%{term}%")
                )
                conditions.append(term_filter)
            
            query = query.filter(and_(*conditions))
    
        # Apply sorting
        certificates = query.order_by(desc(Certificate.date_issued), Resident.last_name).all()
    
        # Format results
        data = []
        for certificate in certificates:
            resident = certificate.resident 
            date_issued = certificate.date_issued
            type = certificate.type
            purpose = certificate.purpose
            resident_name = [
                getattr(resident, "first_name", ""),
                getattr(resident, "middle_name", ""),
                getattr(resident, "last_name", ""),
                getattr(resident, "suffix", "")
            ] if resident else []
    
            full_name = " ".join(filter(None, resident_name))
    
            result = [
                certificate.id,
                date_issued,
                type,
                full_name,
                purpose
            ]
            data.append(result)
        
        self.view.load_table(['id', 'Date Issued', 'Type', 'Resident', 'Purpose'], data)
        
    def add(self):
        add_form = AddCertificateForm()
        
        add_form.form.tbDateIssued.setDate(QDate.currentDate())
        # Populate households for dropdown (household names and IDs)
        residents = self.session.query(Resident).order_by(Resident.first_name).all()
        resident_dict = {
            " ".join(filter(None, [
                resident.first_name,
                resident.middle_name,
                resident.last_name,
                resident.suffix
            ])): resident.id
            for resident in residents
        }
        
        # Set the fields for the form (populate the household dropdown with names)
        add_form.set_fields(name=list(resident_dict.keys()))
        add_form.form.cbName.setCurrentText('')  # Ensure no default value is set
    
        # Button signals
        add_form.addbar.btAdd.clicked.connect(lambda: self.on_add_button_click(add_form, resident_dict))
        add_form.addbar.btCancel.clicked.connect(add_form.reject)
    
        # Execute the form as a modal dialog
        add_form.exec()
    
    def on_add_button_click(self, add_form, resident_dict):
        data = add_form.get_fields()
    
        resident_name = data.get("name")
        if not resident_name:  
            QMessageBox.critical(add_form, "Error", "Please select a Resident.")
            return  
        
        resident_id = resident_dict.get(resident_name)
        if not resident_id:
            QMessageBox.critical(add_form, "Error", f"No matching Resident found for '{resident_name}'.")
            return  
            
        resident = self.session.query(Resident).get(resident_id)
    
        # Remove the 'household' key from the data dictionary since it's already handled
        del data['name']
    
        # Uppercase all string values in data (excluding non-string types)
        data = {key: value.upper() if isinstance(value, str) else value for key, value in data.items()}
    
        # Create a new Resident instance with the provided data
        new_certificate = Certificate(**data)
        new_certificate.resident = resident  # Associate the resident with the selected household
    
        try:
            # Add the new resident to the session and commit the transaction
            self.session.add(new_certificate)
            self.session.commit()
            QMessageBox.information(add_form, "Success", "Certificate added successfully!")
            self.refresh()  
            
            # Close the dialog only if everything is successful
            add_form.accept()
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(add_form, "Error", f"Failed to add resident: {str(e)}")
            add_form.activateWindow() 
            add_form.raise_()    
    
    def edit(self):
        row_id = self.view.get_table_row()
        if row_id:
            certificate = self.session.query(Certificate).get(row_id)
    
            if certificate:
                update_form = UpdateCertificateForm()
    
                # Fetch households
                residents = self.session.query(Resident).order_by(Resident.first_name).all()
                resident_dict = {
                    " ".join(filter(None, [
                        resident.first_name,
                        resident.middle_name,
                        resident.last_name,
                        resident.suffix
                    ])): resident.id
                    for resident in residents
                }
                resident_names = list(resident_dict.keys())
    
                # Populate household combo box
                update_form.form.cbName.clear()
                update_form.form.cbName.addItems(resident_names)
                
                full_name = ""
                
                if Certificate.resident:
                    full_name = " ".join(filter(None, [
                        certificate.resident.first_name,
                        certificate.resident.middle_name,
                        certificate.resident.last_name,
                        certificate.resident.suffix
                    ]))
                    update_form.form.cbName.setCurrentText(full_name)
    
    
                # Set initial values
                update_form.set_fields(
                    name = full_name,
                    date_issued = certificate.date_issued,
                    type = certificate.type,
                    purpose = certificate.purpose
                )
    
                # Revert button restores original values
                update_form.updatebar.btRevert.clicked.connect(
                    lambda: update_form.set_fields(
                        name = full_name,
                        date_issued = certificate.date_issued,
                        type = certificate.type,
                        purpose = certificate.purpose
                    )
                )
    
                # Save button
                update_form.updatebar.btUpdate.clicked.connect(
                    lambda: self.save_update(certificate, update_form, resident_dict)
                )
    
                # Cancel button
                update_form.updatebar.btCancel.clicked.connect(update_form.reject)
    
                update_form.exec()
    
    
    def save_update(self, certificate, update_form, resident_dict):
        updated_data = update_form.get_fields()
    
        # Map household name to ID
        resident_name = update_form.form.cbName.currentText()
        resident_id = resident_dict.get(resident_name)
    
        if not resident_name:
            QMessageBox.critical(update_form, "Error", "Please select a valid resident.")
            return
    
        resident = self.session.query(Resident).get(resident_id)
        if not resident:
            QMessageBox.critical(update_form, "Error", "Selected resident does not exist.")
            return
    
        # Update resident fields
        certificate.date_issued = updated_data['date_issued']
        certificate.type = updated_data['type']
        certificate.purpose = updated_data['purpose']
        certificate.resident = resident
    
        try:
            self.session.commit()
            QMessageBox.information(update_form, "Success", "Certificate updated successfully!")
            update_form.accept()
            self.refresh()
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(update_form, "Error", f"Failed to update Certificate: {str(e)}")
        
    def browse(self):
        row_id = self.view.get_table_row()
        if row_id:
            certificate = self.session.query(Certificate).get(row_id)
            
            if certificate:
                browse_form = BrowseCertificateForm()
                resident = certificate.resident
                
                full_name = " ".join(filter(None, [
                    resident.first_name,
                    resident.middle_name,
                    resident.last_name,
                    resident.suffix
                ]))
                browse_form.set_fields(
                    name = full_name,
                    date_issued = certificate.date_issued,
                    type = certificate.type,
                    purpose = certificate.purpose
                   
                )
                
                browse_form.exec()
    
    def delete(self):
        row_id = self.view.get_table_row()
        if row_id:
            certificate = self.session.query(Certificate).get(row_id)
            if certificate:
                reply = QMessageBox.question(
                    self.view, 
                    "Confirm Deletion",
                    f"Are you sure you want to delete Certificate: {certificate.date_issued} {certificate.type}: {certificate.resident.first_name} {certificate.resident.middle_name} {certificate.resident.last_name} {certificate.resident.suffix}?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
    
                if reply == QMessageBox.Yes:
                    self.session.delete(certificate)
                    self.session.commit()
                    self.refresh()

class AboutUsWindowController:
    def __init__(self, view: AboutWindow):
        self.db = Database()
        self.session = self.db.get_session()
        self.view = view
        self.load_data()

    def load_data(self):
        barangay = self.session.query(Barangay).first()
        users = self.session.query(User).join(User.resident).all()

        user_list = []

        if not users and not barangay:
            return

        for user in users:
            position = user.position
            resident = user.resident
            resident_name = [
                getattr(resident, "first_name", ""),
                getattr(resident, "middle_name", ""),
                getattr(resident, "last_name", ""),
                getattr(resident, "suffix", "")
            ] if resident else []
    
            full_name = " ".join(filter(None, resident_name))

            user_list.append({'name': full_name, 'position': position})
        
        custom_order = ["CAPTAIN", "SECRETARY", "TREASURER", "KAGAWAD", "TANOD"]

        self.view.load_data(
            name = barangay.name,
            history = barangay.history,
            mission = barangay.mission,
            vision = barangay.vision,
            members = sorted(user_list, key=lambda user: custom_order.index(user['position'].upper()) if user['position'].upper() in custom_order else len(custom_order))
        )
            
class SettingsWindowControl:
    def __init__(self, view: SettingsWindow):
        self.view = view
        self.db = Database()
        self.session = self.db.get_session()
        self.load_data()

        self.view.btSave.clicked.connect(self.save_changes)
        self.view.btRevert.clicked.connect(self.revert_changes)
        self.view.btExport.clicked.connect(self.export_csv)
        self.view.btCreateBackup.clicked.connect(self.backup_database)
        self.view.btViewBackup.clicked.connect(self.switch_database)
    
    def load_data(self):
        barangay = self.session.query(Barangay).first()

        if barangay:
            self.view.set_fields(
                name = barangay.name,
                history = barangay.history,
                mission = barangay.mission,
                vision = barangay.vision
            )
    
    def save_changes(self):
        data = self.view.get_fields()
        data = {key: value.upper() if isinstance(value, str) else value for key, value in data.items()}

        barangay = self.session.query(Barangay).first()

        if not barangay:
            barangay = Barangay()
            barangay.name = data.get('name', '')
            barangay.history = data.get('history', '')
            barangay.mission = data.get('mission', '')
            barangay.vision = data.get('vision')

            try:
                # Add the new resident to the session and commit the transaction
                self.session.add(barangay)
                self.session.commit()
                QMessageBox.information(self.view, "Success", "Barangay added successfully!")
                self.load_data()  
                
            except Exception as e:
                self.session.rollback()
                QMessageBox.critical(self.view, "Error", f"Failed to add resident: {str(e)}")
        else:
            barangay.name = data.get('name', '')
            barangay.history = data.get('history', '')
            barangay.mission = data.get('mission', '')
            barangay.vision = data.get('vision')

            try:
                self.session.commit()
                QMessageBox.information(self.view, "Success", "Barangay updated successfully!")
                self.load_data()  
                
            except Exception as e:
                self.session.rollback()
                QMessageBox.critical(self.view, "Error", f"Failed to add resident: {str(e)}")


    def revert_changes(self):
        barangay = self.session.query(Barangay).first()

        if barangay:
            self.view.set_fields(
                name = barangay.name,
                history = barangay.history,
                mission = barangay.mission,
                vision = barangay.vision
            )

    def export_csv(self):
        timestamp = datetime.now().strftime("%Y_%m_%d")

        try:
            # Initialize a Pandas Excel writer to export multiple sheets
            file_path, _ = QFileDialog.getSaveFileName(
                self.view,
                "Save Excel File",
                f"export_{timestamp}.xlsx",
                "Excel Files (*.xlsx);;All Files (*)"
            )

            if not file_path:
                return  # User cancelled

            # Export Resident & Household data
            stmt_resident_household = (
                select(
                    Resident.id.label("resident_id"),
                    Resident.first_name,
                    Resident.last_name,
                    Resident.middle_name,
                    Resident.suffix,
                    Resident.date_of_birth,
                    Resident.occupation,
                    Resident.civil_status,
                    Resident.citizenship,
                    Resident.sex,
                    Resident.education,
                    Resident.remarks,
                    Resident.phone1,
                    Resident.phone2,
                    Resident.email,
                    Resident.role,
                    Household.household_name,
                    Household.house_no,
                    Household.street,
                    Household.sitio,
                    Household.landmark
                )
                .join(Resident.household)
            )
            df_resident_household = pd.read_sql(stmt_resident_household, self.session.bind)

            # Export Resident & Certificate data
            stmt_resident_certificate = (
                select(
                    Resident.id.label("resident_id"),
                    Resident.first_name,
                    Resident.middle_name,
                    Resident.last_name,
                    Resident.suffix,
                    Certificate.type.label("certificate_type"),
                    Certificate.purpose.label("certificate_purpose"),
                    Certificate.date_issued
                )
                .join(Resident.certificates)
            )
            df_resident_certificate = pd.read_sql(stmt_resident_certificate, self.session.bind)

            # Export Blotter data
            stmt_blotter = select(Blotter)
            df_blotter = pd.read_sql(stmt_blotter, self.session.bind)

            # Export Resident & User data
            stmt_resident_user = (
                select(
                    Resident.id.label("resident_id"),
                    Resident.first_name,
                    Resident.last_name,
                    Resident.middle_name,
                    Resident.suffix,
                    Resident.date_of_birth,
                    Resident.occupation,
                    Resident.civil_status,
                    Resident.citizenship,
                    Resident.sex,
                    Resident.education,
                    Resident.remarks,
                    Resident.phone1,
                    Resident.phone2,
                    Resident.email,
                    Resident.role,
                    Household.household_name,
                    Household.house_no,
                    Household.street,
                    Household.sitio,
                    Household.landmark,
                    User.username,
                    User.position
                )
                .join(Resident.user)  
                .join(Resident.household)  
            )
            df_resident_user = pd.read_sql(stmt_resident_user, self.session.bind)

            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df_resident_household.to_excel(writer, sheet_name="RBI", index=False)
                df_resident_certificate.to_excel(writer, sheet_name="Certificates", index=False)
                df_blotter.to_excel(writer, sheet_name="Blotters", index=False)
                df_resident_user.to_excel(writer, sheet_name="Officials", index=False)

            QMessageBox.information(self.view, "Export Successful", f"Data saved to:\n{file_path}")

        except Exception as e:
            # Handle any errors
            QMessageBox.critical(self.view, "Export Failed", str(e))

    def backup_database(self):
        try:
            # Ask the user to select a folder to save the backup
            folder_path = QFileDialog.getExistingDirectory(
                self.view,
                "Select Folder to Save Backup",
                os.path.expanduser("~")  # Default to user's home directory
            )

            if not folder_path:
                return  # User cancelled

            # Get the current timestamp to append to the backup file name
            timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            backup_filename = f"database_backup_{timestamp}.sqlite"

            # Specify the source (current database file) and the destination (selected folder)
            source_db_path = "main.sqlite"  # Adjust with the actual path
            destination_db_path = os.path.join(folder_path, backup_filename)

            # Copy the database to the selected folder
            shutil.copy(source_db_path, destination_db_path)

            # Show a message confirming the backup was successful
            QMessageBox.information(self.view, "Backup Successful", f"Database backed up to:\n{destination_db_path}")

        except Exception as e:
            # Handle any errors
            QMessageBox.critical(self.view, "Backup Failed", str(e))

    def switch_database(self):
        try:
            # Show confirmation dialog with extreme caution warning
            reply = QMessageBox.warning(
                self.view,
                "Extreme Caution!",
                "You are about to replace the current database with another one. "
                "This action cannot be undone! Are you sure you want to continue?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            # If the user selects 'No', exit the function
            if reply == QMessageBox.No:
                return

            # Ask the user to select the backup database (new database file)
            db_path, _ = QFileDialog.getOpenFileName(
                self.view,
                "Select SQLite Database to Replace Current DB",
                "",
                "SQLite Files (*.sqlite *.db *.SQLITE *.DB);;All Files (*)"

            )

            if not db_path:
                return  # User canceled the operation

            # Confirm with a second caution message before proceeding
            confirm = QMessageBox.warning(
                self.view,
                "Extreme Caution!",
                "This will overwrite the current database with the selected one. Are you sure?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if confirm == QMessageBox.No:
                return  # If the user selects 'No', do nothing

            # Copy the selected new database to overwrite the current main.sqlite
            shutil.copy(db_path, 'main.sqlite')

            # Reinitialize the Database singleton to use the new database
            db_instance = Database(db_url='sqlite:///main.sqlite')  # Reuse the default database path
            db_instance.engine.dispose()  # Dispose of the old engine connection
            db_instance.engine = create_engine(f"sqlite:///{db_path}")  # Set the new database
            db_instance.Session = sessionmaker(bind=db_instance.engine)  # Rebind the session to the new engine

            # Notify the user
            QMessageBox.information(None, "Database Switched", "The database has been replaced successfully.")

        except Exception as e:
            # Handle any errors
            QMessageBox.critical(None, "Error", f"Failed to switch databases: {str(e)}")