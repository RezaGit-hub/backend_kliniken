from pydantic import BaseModel
from typing import Optional
from datetime import datetime

#to create new appointment
class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: datetime
    reason: Optional[str] = None

#to get appointment
class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_date: datetime
    reason: Optional[str] = None

    class Config:
        from_attributes = True

#update an appointmnet
class AppointmentUpdate(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    appointment_date: Optional[datetime] = None
    reason: Optional[str] = None
