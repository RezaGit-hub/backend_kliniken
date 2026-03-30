from app.database import get_connection

def create_doctor(data):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
             """INSERT INTO doctors(first_name, last_name, specialization, phone_number)
            VALUES(%s,%s,%s,%s)
            RETURNING id, first_name, last_name, specialization, phone_number""",
            (data.first_name, data.last_name, data.specialization, data.phone_number)
        )

        doctor = cursor.fetchone()

        conn.commit()
        return doctor
    
    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()