from fastapi import FastAPI
from app.database import get_connection
from app.api.patients import router as patient_router
from app.api.doctors import router as doctor_router
from app.api.appointments import router as appointment_router
from app.api import auth
app = FastAPI()

app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(appointment_router)
app.include_router(auth.router, prefix="/auth", tags=["auth"])


"""
@app.get("/")
def root():
    conn = get_connection()
    conn.close()
    return {"message": "DB kliniken Connection ist da...."}


def main():
    print("Kliniken Backend startet...")
    # Hier später FastAPI / Flask App starten

if __name__ == "__main__":
    main()"""