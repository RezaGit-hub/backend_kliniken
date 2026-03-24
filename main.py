from fastapi import FastAPI
from app.database import get_connection
from app.api.patients import router as patient_router

app = FastAPI()

app.include_router(patient_router)


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