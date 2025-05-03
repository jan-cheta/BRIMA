from base import Database
from model import Household, Resident, User, Blotter
from forms import AddHouseholdForm, UpdateHouseholdForm, BrowseHouseholdForm
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
        updated_data = update_form.get_fields()
        
        household.household_name = updated_data['household_name']
        household.house_no = updated_data['house_no']
        household.street = updated_data['street']
        household.sitio = updated_data['sitio']
        household.landmark = updated_data['landmark']
        
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
        updated_data = update_form.get_fields()
        
        household.household_name = updated_data['household_name']
        household.house_no = updated_data['house_no']
        household.street = updated_data['street']
        household.sitio = updated_data['sitio']
        household.landmark = updated_data['landmark']
        
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
        