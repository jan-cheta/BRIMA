from datetime import date
from faker import Faker
import random
from base import Database
from model import Resident, Household, User, Blotter, Certificate, Barangay

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

# Get all created residents to use for certificate and blotter generation
all_residents = session.query(Resident).all()

# Generate Certificates for some residents
for resident in all_residents:
    for _ in range(random.randint(1, 2)):  # 1–2 certificates per resident
        certificate = Certificate(
            date_issued=fake.date_between(start_date='-2y', end_date='today'),
            type=fake.random_element(["Barangay Clearance", "Indigency", "Residency"]).upper(),
            purpose=fake.sentence(nb_words=4).upper(),
            resident=resident
        )
        session.add(certificate)

# Generate 10 blotter records
for _ in range(10):
    complainant = fake.random_element(all_residents)
    respondent = fake.random_element([r for r in all_residents if r.id != complainant.id])
    
    blotter = Blotter(
        record_date=fake.date_between(start_date='-1y', end_date='today'),
        status=fake.random_element(["Open", "Ongoing", "Closed"]).upper(),
        action_taken=fake.sentence(nb_words=6).upper(),
        nature_of_dispute=fake.random_element([
            "Noise Complaint", "Boundary Dispute", "Domestic Issue", "Harassment", "Vandalism"]).upper(),
        complainant=f"{complainant.first_name} {complainant.last_name}".upper(),
        respondent=f"{respondent.first_name} {respondent.last_name}".upper(),
        full_report=fake.paragraph(nb_sentences=3).upper()
    )
    session.add(blotter)

existing_barangay = session.query(Barangay).first()
if not existing_barangay:
    barangay = Barangay(
        name="Brgy Siblot",
        history="Brgy Siblot was established in the early 1900s and has grown into a vibrant, close-knit community.",
        mission="To promote sustainable development, peace, and community welfare.",
        vision="A model barangay characterized by unity, progress, and active citizen participation."
    )
    session.add(barangay)
    session.commit()

session.commit()
