from pydantic import BaseModel
from datetime import date
from typing import Optional

#to create new patient(request)
class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    gender: str
    phone_number: str



#to get patient out(reponse)
class PatientResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: date
    gender: str
    phone_number: str

    class Config:
        from_attributes = True


#to update a patient
class PatientUpdtae(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None