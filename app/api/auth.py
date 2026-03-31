from fastapi import APIRouter, HTTPException
from app.schemas.users import UserCreate, UserLogin
from app.database import get_connection
from app.services.auth_services import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/register")
def register(user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        password_hash = hash_password(user.password)

        cursor.execute(
            """INSERT INTO users(email, password_hash, role) 
            VALUES(%s,%s,%s)
            RETURNING id, email, role""",
            (user.email, password_hash, user.role)
        )

        new_user = cursor.fetchone()
        conn.commit()

        return {
            "id": new_user[0],
            "email": new_user[1],
            "role": new_user[2]
        }

    except Exception:
        conn.rollback()
        raise HTTPException(status_code=500, detail="database error")

    finally:
        cursor.close()
        conn.close()


#to log in accunt role
@router.post("/login")
def login(user: UserLogin):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id, email, password_hash, role FROM users WHERE email = %s",
            (user.email, )
        )

        db_user = cursor.fetchone()


        if not db_user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not verify_password(user.password, db_user[2]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token(
            {"sub": db_user[0], "role": db_user[3]}
        )

        return {"access_token": token}
    
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=500, detail="database error")
    finally:
        cursor.close()
        conn.close()