from fastapi import APIRouter, HTTPException, Depends
from app.database import get_connection
from app.services.auth_dependencies import get_current_user
from app.schemas.patients import PatientCreate, PatientResponse, PatientUpdate
from typing import List


router = APIRouter()

#create a new patient
@router.post("/patients", response_model=PatientResponse)
def create_patient(patient: PatientCreate, current_user = Depends(get_current_user)):

    if current_user["role"] != "admin":
        raise HTTPException(status_code=401, detail="not authorization")
    
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


#read all patients
@router.get("/patients", response_model=List[PatientResponse])
def get_patients(current_user = Depends(get_current_user),
                 page : int= 1,
                 limit : int= 10):
    offset = (page - 1) * limit

    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="not authorization")
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """SELECT id, first_name, last_name, birth_date, gender, phone_number
        FROM patients
        ORDER BY id
        LIMIT %s OFFSET %s
        """,
        (limit, offset)
    )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    patients = []
    for row in rows:
        patients.append({
            "id": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "birth_date": row[3],
            "gender": row[4],
            "phone_number": row[5]
        })

    return patients

#read one patinet with id
@router.get("/patients/{patient_id}")
def get_patient_id(patient_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM patients WHERE id = %s",
        (patient_id, ) 
    )

    patient = cursor.fetchone()
    cursor.close()
    conn.close()

    if not patient:
        raise HTTPException(status_code=404, detail="patient nicht gefunden")
    return {
    "id": patient[0],
    "first_name": patient[1],
    "last_name": patient[2],
    "birth_date": patient[3],
    "gender": patient[4],
    "phone_number": patient[5]
}


#read one patient with lastname
@router.get("/patients/last_name/{last_name}")
def get_patient_lastname(last_name: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients WHERE last_name = %s", (last_name, ))

    patient = cursor.fetchone()
    cursor.close()
    conn.close()

    if not patient:
        raise HTTPException(status_code=404, detail="patient nicht gefunden")
    return patient

#update any patient
@router.put("/patients/{patient_id}")
def update_patient(patient_id: int, patient: PatientUpdate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """UPDATE patients
        SET first_name = COALESCE(%s, first_name),
        last_name = COALESCE(%s, last_name),
        birth_date = COALESCE(%s, birth_date),
        gender = COALESCE(%s, gender),
        phone_number = COALESCE(%s, phone_number)
        WHERE id = %s
        RETURNING id, first_name, last_name, birth_date, gender, phone_number
        """,
        (patient.first_name, patient.last_name, patient.birth_date, patient.gender, patient.phone_number, patient_id)
    )

    updated= cursor.fetchone()
    conn.commit()

    cursor.close()
    conn.close()

    if not updated:
        raise HTTPException(status_code=404, detail="patient nicht gefunden")
    return {
        "id": updated[0],
        "first_name": updated[1],
        "last_name": updated[2],
        "birth_date": updated[3],
        "gender": updated[4],
        "phone_number": updated[5]
    }

#delet one patient
@router.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE id = %s RETURNING id;", (patient_id,)
    )

    deleted = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if not deleted:
        raise HTTPException(status_code=404, detail="patient nicht gefunden")
    return{"message": "patient wurde gelöscht"}
