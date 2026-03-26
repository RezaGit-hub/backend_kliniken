from fastapi import APIRouter , HTTPException
from app.database import get_connection
from app.schemas.appointments import AppointmentCreate,AppointmentResponse,AppointmentUpdate
from typing import List
router = APIRouter()

@router.post("/appointments", response_model=AppointmentResponse)
def create_appointment(appointment: AppointmentCreate):
    conn = get_connection()
    cursor= conn.cursor()

    try:
        cursor.execute(
            """INSERT INTO appointments(patient_id, doctor_id, appointment_date, reason
             VALUES(%s,%s,%s,%s)
              RETURNING id, patient_id, doctor_id, appointment_date, reason""",
              (appointment.patient_id, appointment.doctor_id, appointment.appointment_date, appointment.reason )
        )

        new_appointment = cursor.fetchone()
        conn.commit()

        return{
            "id": new_appointment[0],
            "patient_id": new_appointment[1],
            "doctor_id": new_appointment[2],
            "appointment_date": new_appointment[3],
            "reason": new_appointment[4]
        }
    
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="database error")
    
    finally:
        cursor.close()
        conn.close()

#to read all appointments
@router.get("/appointments", response_model=List[AppointmentResponse])
def get_appointments():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """SELECT id, patient_id, doctor_id, appointment_date, reason
        FROM appointments
        ORDER BY id"""
    )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    appointments= []
    for row in rows:
        appointments.append({
            "id": row[0],
            "patient_id": row[1],
            "doctor_id": row[2],
            "appointment_date": row[3],
            "reason": row[4]
        })
    return appointments


#to read an appointment with id
@router.get("/appointments/{appointment_id}")
def get_appointment(appointment_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM appointments WHERE id = %s", (appointment_id,))

    appointment = cursor.fetchone()
    cursor.close()
    conn.close()

    if not appointment:
        raise HTTPException(status_code=404, detail="appointment nicht gefunden")
    return{
        "id": appointment[0],
        "patient_id": appointment[1],
        "doctor_id": appointment[2],
        "appointment_date": appointment[3],
        "reason": appointment[4]
    }

    

#to read an appointment with patient_id
@router.get("/appointments/patient/{patient_id}")
def get_appointment_patientId(patient_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM appointments WHERE patient_id = %s", (patient_id, ))

    appointment = cursor.fetchall()
    cursor.close()
    conn.close()

    if not appointment:
        raise HTTPException(status_code=404, detail="keine Appointment gefunden")
    return appointment


#to update an appointment
@router.put("/appointments/{appointment_id}")
def update_appointment(appointment_id: int,appointment:AppointmentUpdate ):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """UPDATE appointments
        SET patient_id = COALESCE(%s, patient_id),
        doctor_id = COALESCE(%s, doctor_id),
        appointment_date = COALESCE(%s, appointment_date),
        reason=COALESCE(%s, reason)
        WHERE id = %s
        RETURNING id, patient_id, doctor_id, appointment_date, reason"""
        (appointment.patient_id, appointment.doctor_id, appointment.appointment_date, appointment.reason, appointment_id)
    )

    updated = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if not updated:
        raise HTTPException(status_code=404, detail="appointment nicht gefunden")
    return{
        "id": updated[0],
        "patient_id": updated[1],
        "doctor_id": updated[2],
        "appointment_date": updated[3],
        "reason": updated[4]
    }


#to delete an appointment
@router.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """DELETE FROM appointments WHERE id = %s 
        RETURNING id """, (appointment_id, )
    )

    deleted = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if not deleted:
        raise HTTPException(status_code=404, detail="appointment nicht gefunden")
    return{"message: ": "appointment wurde gelöscht"}

