from fastapi import APIRouter, HTTPException, Depends
from app.database import get_connection
from app.schemas.doctors import DoctorCreate, DoctorResponse, DoctorUpdate

router = APIRouter()
#to create new doctor
@router.post("/doctors", response_model=DoctorResponse)
def create_doctor(doctor: DoctorCreate):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """INSERT INTO doctors(first_name, last_name, specialization, phone_number)
            VALUES(%s,%s,%s,%s)
            RETURNING id, first_name, last_name, specialization, phone_number""",
            (doctor.first_name, doctor.last_name, doctor.specialization, doctor.phone_number)
        )

        new_doctor = cursor.fetchone()
        conn.commit()

        return{
            "id": new_doctor[0],
            "first_name": new_doctor[1],
            "last_name": new_doctor[2],
            "specialization": new_doctor[3],
            "phone_number": new_doctor[4]
        }

    except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=201, detail= "database error")
    finally:
         cursor.close()
         conn.close()


#to get doctors
@router.get("/doctors", response_model=DoctorResponse)
def get_doctors():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
          """SELECT id, first_name, last_name, specialization, phone_number
          FROM doctors
          ORDER BY id"""
     )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    doctors = []

    for row in rows:
          doctors.append({
               "id": row[0],
               "first_name": row[1],
               "last_name": row[2],
               "specialization": row[3],
               "phone_number": row[4]
          })

    return doctors


#to get a doctor with id
@router.get("/doctors/{doctor_id}")
def get_doctor_id(doctor_id:int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM doctors WHERE id = %s",
                    (doctor_id, ))
    doctor = cursor.fetchone()
    cursor.close()
    conn.close()

    if not doctor:
         raise HTTPException(status_code=404, detail="doctor nicht gefunden")
    return{
         "id": doctor[0],
         "first_name": doctor[1],
         "last_name": doctor[2],
         "specialization": doctor[3],
         "phone_number": doctor[4]
    }


#read a doctor whit lastname
@router.get("/doctors/last_name/{last_name}")
def get_doctor_lastname(last_name: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM doctors WHERE last_name = %s", (last_name, ))

    doctor = cursor.fetchone()
    cursor.close()
    conn.close()

    if not doctor:
         raise HTTPException(status_code=404, detail="doctor nicht gefunden")
    return doctor

#update doctor
@router.put("/doctors/{doctor_id}")
def update_doctor(doctor_id:int, doctor:DoctorUpdate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
          """UPDATE doctors
          SET first_name = COALESCE(%s, first_name),
          last_name = COALESCE(%s, last_name),
          specialization = COALESCE(%s, specialization),
          phone_number = COALESCE(%s, phone_number)""",
          doctor.first_name, doctor.last_name, doctor.specialization, doctor.phone_number, doctor_id
     )
    
    updated = cursor.fetchone()
    conn.commit()

    cursor.close()
    conn.close()

    if not updated:
         raise HTTPException(status_code=404, detail="doctor nicht gefunden")
    return{
         "id": updated[0],
         "first_name": updated[1],
         "last_name": updated[2],
         "specialization": updated[3],
         "phone_number": updated[4]
    }


@router.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id:int):
     conn = get_connection()
     cursor = conn.cursor()

     cursor.execute("" \
     "DELETE FROM doctors WHERE id = %s RETURNING id;", (doctor_id))

     deleted = cursor.fetchone()
     conn.commit()
     cursor.close()
     conn.close()

     if not deleted:
          raise HTTPException(status_code=204, detail="doctor nicht gefunden")
     return{"message: ": "doctor wurde gelöscht"}