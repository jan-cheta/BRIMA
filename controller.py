from base import Database
from model import Household, Resident, User, Blotter
from forms import AddHouseholdForm, UpdateHouseholdForm
from view import  BrimaView
from widgets import BaseWindow
from PySide6.QtWidgets import QMessageBox, QDialog


class MainController:
    def __init__(self, view : BrimaView):
        self.db = Database()
        self.session = self.db.get_session()
        self.view = view
        self.household_control = HouseholdWindowController(self.view.household_window)
        

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
            search_text = self.view.get_search_text().lower()  # Get the search text and convert to lowercase
            search_terms = search_text.split()  # Split search text by spaces into separate terms
        
            # Start the query
            query = self.session.query(Household).order_by(Household.household_name)
            
            # Apply filters for each search term
            for term in search_terms:
                query = query.filter(
                    Household.household_name.ilike(f"%{term}%") |  # Search by household name
                    Household.house_no.ilike(f"%{term}%") |       # Search by house number
                    Household.street.ilike(f"%{term}%") |         # Search by street
                    Household.sitio.ilike(f"%{term}%") |           # Search by sitio
                    Household.landmark.ilike(f"%{term}%")         # Search by landmark
                )
            
            # Execute the query
            households = query.all()
            
            # Prepare the data to display in the table
            data = []
            for household in households:
                result = [
                    household.id,
                    household.household_name,
                    f"{household.house_no} {household.street} {household.sitio} {household.landmark}"
                ]
                data.append(result)
            
            # Load the filtered data into the table
            self.view.load_table(['id', 'Household Name', 'Address'], data)
    
    def add(self):
            # Create and show the add household form
            add_form = AddHouseholdForm()
            add_form.addbar.btAdd.clicked.connect(add_form.accept)
            add_form.addbar.btCancel.clicked.connect(add_form.reject)
            
            # Execute the form as a modal dialog
            if add_form.exec() == QDialog.Accepted:
                # Get the data from the form
                data = add_form.get_fields()
                
                # Create a new Household object with the data
                new_household = Household(**data)
                
                # Add to the session and commit to the database
                try:
                    self.session.add(new_household)
                    self.session.commit()
                    
                    # Refresh the view with the updated data
                    self.refresh()
                except Exception as e:
                    # Handle any database errors (e.g., unique constraints)
                    self.session.rollback()
                    QMessageBox.critical(self.view, "Error", f"Failed to add household: {str(e)}")

    
    def edit(self):
        row_id = self.view.get_table_row()
        if row_id:
            # Query the selected household from the database
            household = self.session.query(Household).get(row_id)
            
            if household:
                # Create and show the update form
                update_form = UpdateHouseholdForm()
                
                # Populate the form with the current data
                update_form.set_fields(
                    household_name=household.household_name,
                    house_no=household.house_no,
                    street=household.street,
                    sitio=household.sitio,
                    landmark=household.landmark
                )
                
                # Connect the revert button to reset fields to original values
                update_form.updatebar.btRevert.clicked.connect(
                    lambda: update_form.set_fields(
                        household_name=household.household_name,
                        house_no=household.house_no,
                        street=household.street,
                        sitio=household.sitio,
                        landmark=household.landmark
                    )
                )
                
                # Connect the update button to accept the form and save changes
                update_form.updatebar.btUpdate.clicked.connect(
                    lambda: self.save_update(household, update_form)
                )
                
                # Connect the cancel button to reject and close the form without saving
                update_form.updatebar.btCancel.clicked.connect(update_form.reject)
                
                # Show the form and wait for the result (Accepted or Rejected)
                if update_form.exec() == QDialog.Accepted:
                    # The form was accepted, you might want to refresh the view
                    self.refresh()
    
    def save_update(self, household, update_form):
        # Get the updated data from the form
        updated_data = update_form.get_fields()
        
        # Update the household object with the new data
        household.household_name = updated_data['household_name']
        household.house_no = updated_data['house_no']
        household.street = updated_data['street']
        household.sitio = updated_data['sitio']
        household.landmark = updated_data['landmark']
        
        # Commit the changes to the database
        try:
            self.session.commit()
            QMessageBox.information(self.view, "Success", "Household updated successfully!")
        except Exception as e:
            self.session.rollback()  # Rollback in case of error
            QMessageBox.critical(self.view, "Error", f"Failed to update household: {str(e)}")
        
        # Close the form after updating
        update_form.accept()   
        
    def browse(self):
        pass
        
    
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
