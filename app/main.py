from typing import List

from fastapi import Depends, Request, Response, FastAPI
from sqlalchemy.orm import Session  # Asegúrate de importar desde sqlalchemy.orm
from fastapi import FastAPI, HTTPException

from BBDD.mysql import crud, schemas
from BBDD.mysql.crud import get_artista_marcial_by_dni, artista_marcial_exists, create_artista_marcial, \
    get_all_escuelas, get_escuela_by_id, create_escuela, delete_artista_marcial_by_dni, delete_artista_marcial_by_id, \
    delete_escuela_by_id, update_password_by_dni
from BBDD.mysql.database import SessionLocal, engine, Base
from BBDD.mysql.models import ArtistaMarcial
from BBDD.mysql.schemas import ArtistaMarcialInDB, ArtistaMarcialCreate, EscuelaInDB, EscuelaCreate

app = FastAPI()

# Crear las tablas automáticamente
Base.metadata.create_all(bind=engine)


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


# TODO ARTISTAS MARCIALES
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


# Eliminar artista por DNI
@app.delete("/artistas-marciales/dni/{dni}")
def delete_artista_marcial_dni(dni: str, db: Session = Depends(get_db)):
    return delete_artista_marcial_by_dni(db, dni)


# Eliminar artista por ID
@app.delete("/artistas-marciales/id/{artista_id}")
def delete_artista_marcial_id(artista_id: int, db: Session = Depends(get_db)):
    return delete_artista_marcial_by_id(db, artista_id)


@app.put("/artistas-marciales/{dni}/contrasena")
def update_artista_contrasena(dni: str, new_password: str, db: Session = Depends(get_db)):
    # Llamamos al método CRUD para actualizar la contraseña
    artista_actualizado = update_password_by_dni(db, dni, new_password)

    return {"message": "Contraseña actualizada correctamente", "artista": artista_actualizado}


# TODO ESCUELAS

@app.get("/escuelas", response_model=List[EscuelaInDB])
def read_escuelas(db: Session = Depends(get_db)):
    # Llamar al método CRUD para obtener todas las escuelas
    escuelas = get_all_escuelas(db)
    if not escuelas:
        raise HTTPException(status_code=404, detail="No se encontraron escuelas")

    return escuelas


@app.get("/escuelas/{escuela_id}", response_model=EscuelaInDB)
def read_escuela(escuela_id: int, db: Session = Depends(get_db)):
    # Llamar al método CRUD para obtener la escuela por su ID
    escuela = get_escuela_by_id(db, escuela_id)

    # Si la escuela no existe, lanzar un error 404
    if escuela is None:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")

    return escuela


@app.post("/escuelas/", response_model=EscuelaInDB)
def create_new_escuela(escuela: EscuelaCreate, db: Session = Depends(get_db)):
    # Llamar al método CRUD para crear la escuela
    nueva_escuela = create_escuela(db, escuela)

    return nueva_escuela


# Eliminar escuela por ID
@app.delete("/escuelas/{escuela_id}")
def delete_escuela(escuela_id: int, db: Session = Depends(get_db)):
    return delete_escuela_by_id(db, escuela_id)
