from app.database import get_connection

def create_patients(data):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """INSERT INTO patients(first_name, last_name, birth_date, gender, phone_number)
                 VALUES(%s,%s,%s,%s,%s)
                  RETURNING id, first_name, last_name, birth_date, gender, phone_number""",
                  (data.first_name, data.last_name, data.birth_date, data.gender, data.phone_number)
            )
        
        patient = cursor.fetchone()
        conn.commit()

        return patient

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()