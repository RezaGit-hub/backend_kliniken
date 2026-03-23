from fastapi import APIRouter, HTTPException, Depends
from app.database import get_connection
from datetime import date
from app.schemas.patients import PatientCreate, PatientResponse, PatientUpdate
from typing import List

router = APIRouter()

#create a new patient
@router.post("/patients", response_model=PatientResponse)
def create_patient(patient: PatientCreate):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """INSERT INTO patients(first_name, last_name, birth_date, gender, phone_number)
             VALUES(%s,%s,%s,%s,%s)
              RETURNING id, first_name, last_name, birth_date, gender, phone_number""",
              (patient.first_name, patient.last_name, patient.birth_date, patient.gender, patient.phone_number)
        )

        new_patient = cursor.fetchone()
        conn.commit()

        return{
            "id": new_patient[0],
            "first_name": new_patient[1],
            "last_name": new_patient[2],
            "birth_date": new_patient[3],
            "gender": new_patient[4],
            "phone_number": new_patient[5]
        }
    
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Database error")
    
    finally:
        cursor.close()
        conn.close()