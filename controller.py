from base import Database
from model import Household, Resident, User, Blotter
from forms import (AddHouseholdForm, AddResidentForm, BrowseResidentForm,
    UpdateHouseholdForm, BrowseHouseholdForm, UpdateResidentForm)
from view import  BrimaView
from widgets import BaseWindow
from PySide6.QtWidgets import QMessageBox, QDialog
from sqlalchemy import or_, and_


class MainController:
    def __init__(self, view : BrimaView):
        self.db = Database()
        self.session = self.db.get_session()
        self.view = view
        self.household_control = HouseholdWindowController(self.view.household_window)
        self.resident_control = ResidentWindowController(self.view.resident_window)
        
        self.view.btHousehold.clicked.connect(lambda: self.view.stack.setCurrentIndex(0))
        self.view.btResident.clicked.connect(lambda: self.view.stack.setCurrentIndex(1))

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
            QMessageBox.critical(self.view, "Error", "Please select a Household.")
            return  # Exit if the household is not selected or invalid
        
        # Retrieve the corresponding Household ID from the dictionary
        household_id = household_dict.get(household_name)
        if not household_id:
            QMessageBox.critical(self.view, "Error", f"No matching Household found for '{household_name}'.")
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
            self.refresh()  # Refresh the view/list of residents
    
            # Close the dialog only if everything is successful
            add_form.accept()
        except Exception as e:
            # If any error occurs, roll back the session and display an error message
            self.session.rollback()
            QMessageBox.critical(self.view, "Error", f"Failed to add resident: {str(e)}")
    
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
            QMessageBox.critical(self.view, "Error", "Please select a valid household.")
            return
    
        household = self.session.query(Household).get(household_id)
        if not household:
            QMessageBox.critical(self.view, "Error", "Selected household does not exist.")
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
            QMessageBox.information(self.view, "Success", "Resident updated successfully!")
            update_form.accept()
            self.refresh()
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(self.view, "Error", f"Failed to update resident: {str(e)}")
        
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
        pass
        
    def search(self):
        pass
    
    def add(self):
        pass
    
    def edit(self):
        pass
    
    def delete(self):
        pass
    
    def browse(self):
        pass