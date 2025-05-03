from datetime import date
from faker import Faker
from base import Database
from model import Resident, Household

# Initialize Faker
fake = Faker("en_PH")  # Philippine locale, fallback to 'en' if this fails

# Phone number generator (since msisdn/phone_number may not be available)
def generate_ph_mobile():
    return fake.numerify("09#########")  # Simulate a valid PH mobile number

# Connect to the database
db = Database()
session = db.get_session()

# Sample sitios and landmarks for variety
sitios = ["Sitio Uno", "Sitio Dos", "Sitio Tres", "Purok 4", "Zone 5"]
landmarks = ["Near Barangay Hall", "Beside Elementary School", "Behind Chapel", "Near Basketball Court"]

# Create 20 households with 2 residents each
for i in range(20):
    household = Household(
        household_name=f"Family of {fake.last_name()}",
        house_no=str(fake.building_number()),
        street=fake.street_name(),
        sitio=fake.random_element(sitios),
        landmark=fake.random_element(landmarks)
    )

    for j in range(2):
        sex = fake.random_element(["Male", "Female"])
        resident = Resident(
            first_name=fake.first_name_male() if sex == "Male" else fake.first_name_female(),
            last_name=household.household_name.replace("Family of ", ""),
            middle_name=fake.last_name(),
            suffix=fake.random_element(["Jr.", "Sr.", "III", ""]),
            data_of_birth=fake.date_of_birth(minimum_age=20, maximum_age=80),
            occupation=fake.job(),
            civil_status=fake.random_element(["Single", "Married", "Widowed", "Divorced"]),
            citizenship="Filipino",
            sex=sex,
            education=fake.random_element([
                "High School", "Bachelor's Degree", "Master's Degree", "PhD", "Associate's Degree"]),
            remarks=fake.sentence(nb_words=6),
            phone1=generate_ph_mobile(),
            phone2=generate_ph_mobile(),
            email=fake.email(),
        )
        resident.household = household

    session.add(household)

# Commit all at once
session.commit()
