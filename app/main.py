from fastapi import Depends, Request, Response, FastAPI
from sqlalchemy.orm import Session  # Asegúrate de importar desde sqlalchemy.orm
from fastapi import FastAPI, HTTPException

from BBDD.mysql import crud, schemas
from BBDD.mysql.crud import get_artista_marcial_by_dni, artista_marcial_exists, create_artista_marcial
from BBDD.mysql.database import SessionLocal, engine, Base
from BBDD.mysql.models import ArtistaMarcial
from BBDD.mysql.schemas import ArtistaMarcialInDB, ArtistaMarcialCreate

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
        print("Hello World")
    finally:
        db.close()


@app.get("/artistas")
def read_artistas(db: Session = Depends(get_db)):
    # Aquí iría tu lógica para consultar la base de datos
    return {"artistas": "Aquí irían los datos de los artistas"}


@app.get("/artistas-marciales/{dni}", response_model=schemas.ArtistaMarcialInDB)
def read_artista_marcial(dni: str, db: Session = Depends(get_db)):
    # Llamada al método CRUD para obtener el artista por DNI
    artista = get_artista_marcial_by_dni(db, dni)

    if artista is None:
        raise HTTPException(status_code=404, detail="Artista marcial no encontrado")

    return artista


@app.get("/artistas-marciales/existe/{dni}", response_model=bool)
def check_artista_marcial_exists(dni: str, db: Session = Depends(get_db)):
    # Llamada al método CRUD para verificar si existe
    if artista_marcial_exists(db, dni):
        return True
    return False


@app.post("/artistas-marciales/", response_model=ArtistaMarcialInDB)
def create_artista(artista: ArtistaMarcialCreate, db: Session = Depends(get_db)):
    # Verificar si el artista ya existe por DNI
    artista_existente = db.query(ArtistaMarcial).filter(ArtistaMarcial.dni == artista.dni).first()

    if artista_existente:  # Si existe un artista con el mismo dni
        raise HTTPException(status_code=400, detail="El artista marcial con este DNI ya existe")

    # Crear el artista marcial
    nuevo_artista = create_artista_marcial(db, artista)

    return nuevo_artista
