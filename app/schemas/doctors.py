from pydantic import BaseModel
from typing import Optional


#to create new doctor(post/request)
class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    specialization:str
    phone_number: str


#to get doctors
class DoctorResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    specialization: str
    phone_number: str

    class Config:
        from_attributes = True

#to update doctor   
class DoctorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    specialization: Optional[str] = None
    phone_number: Optional[str] = None


#