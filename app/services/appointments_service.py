from app.database import get_connection

def create_appointment(data):
    conn = get_connection()
    cursor= conn.cursor()

    try:
        cursor.execute(
            """INSERT INTO appointments(patient_id, doctor_id, appointment_date, reason)
             VALUES(%s,%s,%s,%s)
              RETURNING id, patient_id, doctor_id, appointment_date, reason""",
              (data.patient_id, data.doctor_id, data.appointment_date, data.reason )
        )

        appointment = cursor.fetchone()
        conn.commit()

        return appointment
    
    except Exception as e:
        conn.rollback()
        raise
    
    finally:
        cursor.close()
        conn.close()


def get_appointments_details():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """SELECT 
            a.id,
            p.first_name || ' ' || p.last_name AS patient_name,
            d.first_name || ' ' || d.last_name AS doctor_name,
            a.appointment_date,
            a.reason
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            JOIN doctors d ON a.doctor_id = d.id
            ORDER BY a.id"""
        )
        return cursor.fetchall()
    
    finally:
        cursor.close()
        conn.close()