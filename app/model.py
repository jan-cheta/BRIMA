from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from base import Base
import datetime

class BaseModel(Base):
    __abstract__ = True
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True)
    date_added = Column(Date, default=datetime.date.today)

class Barangay(BaseModel):
    __tablename__ = 'barangay'

    name = Column(String)
    history = Column(String)
    mission = Column(String)
    vision = Column(String)

class Resident(BaseModel):
    __tablename__ = "residents"


    first_name = Column(String)
    last_name = Column(String)
    middle_name = Column(String)
    suffix = Column(String)
    date_of_birth = Column(Date)
    occupation = Column(String)
    civil_status = Column(String)
    citizenship = Column(String)
    sex = Column(String)
    education = Column(String)
    remarks = Column(String)
    phone1 = Column(String)
    phone2 = Column(String)
    email = Column(String)
    role = Column(String)
    household_id = Column(ForeignKey("households.id"))
    
    household = relationship("Household", back_populates="residents")
    user = relationship("User", back_populates='resident')
    certificates = relationship("Certificate")


class Household(BaseModel):
    __tablename__ = "households"

    household_name = Column(String)
    house_no = Column(String)
    street = Column(String)
    sitio = Column(String)
    landmark = Column(String)
    residents = relationship(Resident)

class User(BaseModel):
    __tablename__ = "users"

    username = Column(String, unique=True)
    password = Column(String)
    position = Column(String)
    resident_id = Column(ForeignKey("residents.id"), unique=True)
    
    resident = relationship("Resident", back_populates='user', uselist=False)

class Blotter(BaseModel):
    __tablename__ = "blotters"

    record_date = Column(Date)
    status = Column(String)
    action_taken = Column(String)
    nature_of_dispute = Column(String)
    complainant = Column(String)
    respondent = Column(String)
    full_report = Column(String)
    
class Certificate(BaseModel):
    __tablename__ = "certificates"
    
    date_issued = Column(Date)
    type = Column(String)
    purpose = Column(String)
    resident_id = Column(ForeignKey("residents.id"))
    
    resident = relationship("Resident", back_populates='certificates')




