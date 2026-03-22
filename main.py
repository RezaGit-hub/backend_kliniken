from fastapi import FastAPI
from app.database import get_connection

app = FastAPI()

@app.get("/")
def root():
    conn = get_connection()
    conn.close()
    return {"message": "DB kliniken Connection ist da...."}

"""
def main():
    print("Kliniken Backend startet...")
    # Hier später FastAPI / Flask App starten

if __name__ == "__main__":
    main()"""