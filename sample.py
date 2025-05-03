from datetime import date
from base import Database
from model import Resident, Household

# Connect to the database
db = Database()
session = db.get_session()

# Create 20 households with 2 residents each
for i in range(20):
    household = Household(household_name=f"Household {i}")
    for j in range(2):
        resident = Resident(
            first_name=f"Resident {j+1}",
            last_name="Smith",
            middle_name="J.",
            suffix="III",
            data_of_birth=date(1980, 1, 1),  # ✅ use datetime.date object
            occupation="Civil Engineer",
            civil_status="Married",
            citizenship="Filipino",
            sex="Male",
            education="Bachelor's Degree",
            remarks="No Remarks",
            phone1="09123456789",
            phone2="09123456789",
            email="resident@gmail.com",
        )
        resident.household = household
    session.add(household)

session.commit()
