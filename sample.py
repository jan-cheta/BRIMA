from datetime import date
from faker import Faker
from base import Database
from model import Resident, Household, User

# Initialize Faker
fake = Faker("en_PH")  # Philippine locale

def generate_ph_mobile():
    return fake.numerify("09#########")

# Connect to the database
db = Database()
session = db.get_session()

sitios = ["Sitio Uno", "Sitio Dos", "Sitio Tres", "Purok 4", "Zone 5"]
landmarks = ["Near Barangay Hall", "Beside Elementary School", "Behind Chapel", "Near Basketball Court"]
positions = ["Captain", "Secretary", "Treasurer", "Kagawad", "Tanod"]

# Create 20 households with 2 residents each; one resident gets a User
for i in range(20):
    household = Household(
        household_name=f"FAMILY OF {fake.last_name().upper()}",
        house_no=str(fake.building_number()).upper(),
        street=fake.street_name().upper(),
        sitio=fake.random_element(sitios).upper(),
        landmark=fake.random_element(landmarks).upper()
    )

    for j in range(2):
        sex = fake.random_element(["Male", "Female"])
        first_name = fake.first_name_male() if sex == "Male" else fake.first_name_female()
        resident = Resident(
            first_name=first_name.upper(),
            last_name=household.household_name.replace("FAMILY OF ", ""),
            middle_name=fake.last_name().upper(),
            suffix=fake.random_element(["Jr.", "Sr.", "III", ""]).upper(),
            date_of_birth=fake.date_of_birth(minimum_age=20, maximum_age=80),
            occupation=fake.job().upper(),
            civil_status=fake.random_element(["Single", "Married", "Widowed", "Divorced"]).upper(),
            citizenship="FILIPINO",
            sex=sex.upper(),
            education=fake.random_element([
                "High School", "Bachelor's Degree", "Master's Degree", "PhD", "Associate's Degree"]).upper(),
            remarks=fake.sentence(nb_words=6).upper(),
            phone1=generate_ph_mobile(),
            phone2=generate_ph_mobile(),
            email=fake.email().upper(),
        )
        resident.household = household

        # Only create a user account for the first resident in each household
        if j == 0:
            username = f"{resident.first_name.lower()}{resident.last_name.lower()}{fake.random_int(100, 999)}"
            user = User(
                username=username,
                password="password123",  # In production, always hash passwords!
                position=fake.random_element(positions),
                resident=resident
            )
            session.add(user)

    session.add(household)

session.commit()
