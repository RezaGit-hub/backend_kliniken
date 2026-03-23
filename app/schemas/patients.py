from pydantic import BaseModel
from datetime import date
from typing import Optional

#to create new patient(request)
class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    gender: str
    phone_number: int


#to get patient out(reponse)
class PatientResponse(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    gender: str
    phone_number: int 

    class Config:
        from_attributes = True


#to update a patient
class PatientUpdtae(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    gender: str
    phone_number: int