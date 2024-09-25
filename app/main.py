from datetime import datetime
from typing import List

import pymongo
from fastapi import Depends, Request, Response, FastAPI
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException

from BBDD.mongodb.database import chats
from BBDD.mongodb.models import DiccionarioInsertar, Mensaje
from BBDD.mysql import schemas, crud
from BBDD.mysql.crud import get_artista_marcial_by_dni, artista_marcial_exists, create_artista_marcial, \
    get_all_escuelas, get_escuela_by_id, create_escuela, delete_artista_marcial_by_dni, delete_artista_marcial_by_id, \
    delete_escuela_by_id, update_password_by_dni
from BBDD.mysql.database import SessionLocal, engine, Base
from BBDD.mysql.models import ArtistaMarcial
from BBDD.mysql.schemas import ArtistaMarcialInDB, ArtistaMarcialCreate, EscuelaInDB, EscuelaCreate

# ResultadoCompeticionResponse

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
    finally:
        db.close()


#
#
# TODO MYSQL
#
#

# TODO ARTISTAS MARCIALES
@app.get("/artistas")
def read_artistas(db: Session = Depends(get_db)):
    # Obtener: Consulta para obtener todos los artistas marciales
    return {"artistas": "Aquí irían los datos de los artistas"}


@app.get("/artistas-marciales/{dni}", response_model=schemas.ArtistaMarcialInDB)
def read_artista_marcial(dni: str, db: Session = Depends(get_db)):
    # Obtener: Llamada al método CRUD para obtener el artista por DNI
    artista = get_artista_marcial_by_dni(db, dni)

    if artista is None:
        raise HTTPException(status_code=404, detail="Artista marcial no encontrado")

    return artista


@app.get("/artistas-marciales/existe/{dni}", response_model=bool)
def check_artista_marcial_exists(dni: str, db: Session = Depends(get_db)):
    # Verificar: Llamada al método CRUD para verificar si el artista marcial existe por DNI
    return artista_marcial_exists(db, dni)


@app.post("/artistas-marciales/", response_model=ArtistaMarcialInDB)
def create_artista(artista: ArtistaMarcialCreate, db: Session = Depends(get_db)):
    # Crear: Crear un nuevo artista marcial
    artista_existente = db.query(ArtistaMarcial).filter(ArtistaMarcial.dni == artista.dni).first()

    if artista_existente:
        raise HTTPException(status_code=400, detail="El artista marcial con este DNI ya existe")

    nuevo_artista = create_artista_marcial(db, artista)
    return nuevo_artista


# Eliminar artista por DNI
@app.delete("/artistas-marciales/dni/{dni}")
def delete_artista_marcial_dni(dni: str, db: Session = Depends(get_db)):
    # Eliminar: Eliminar un artista marcial por su DNI
    return delete_artista_marcial_by_dni(db, dni)


# Eliminar artista por ID
@app.delete("/artistas-marciales/id/{artista_id}")
def delete_artista_marcial_id(artista_id: int, db: Session = Depends(get_db)):
    # Eliminar: Eliminar un artista marcial por su ID
    return delete_artista_marcial_by_id(db, artista_id)


@app.put("/artistas-marciales/{dni}/contrasena")
def update_artista_contrasena(dni: str, new_password: str, db: Session = Depends(get_db)):
    # Actualizar: Actualizar la contraseña de un artista marcial por su DNI
    artista_actualizado = update_password_by_dni(db, dni, new_password)
    return {"message": "Contraseña actualizada correctamente", "artista": artista_actualizado}


# TODO ESCUELAS

@app.get("/escuelas", response_model=List[EscuelaInDB])
def read_escuelas(db: Session = Depends(get_db)):
    # Obtener: Llamar al método CRUD para obtener todas las escuelas
    escuelas = get_all_escuelas(db)
    if not escuelas:
        raise HTTPException(status_code=404, detail="No se encontraron escuelas")
    return escuelas


@app.get("/escuelas/{escuela_id}", response_model=EscuelaInDB)
def read_escuela(escuela_id: int, db: Session = Depends(get_db)):
    # Obtener: Llamar al método CRUD para obtener una escuela por su ID
    escuela = get_escuela_by_id(db, escuela_id)

    if escuela is None:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")

    return escuela


@app.post("/escuelas/", response_model=EscuelaInDB)
def create_new_escuela(escuela: EscuelaCreate, db: Session = Depends(get_db)):
    # Crear: Crear una nueva escuela
    nueva_escuela = create_escuela(db, escuela)
    return nueva_escuela


# Eliminar escuela por ID
@app.delete("/escuelas/{escuela_id}")
def delete_escuela(escuela_id: int, db: Session = Depends(get_db)):
    # Eliminar: Eliminar una escuela por su ID
    return delete_escuela_by_id(db, escuela_id)


# TODO COMPETICIONES

# Obtener todas las competiciones
@app.get("/competiciones", response_model=List[schemas.CompeticionInDB])
def read_competiciones(db: Session = Depends(get_db)):
    return crud.get_all_competiciones(db)


# Obtener una competición por ID
@app.get("/competiciones/{competicion_id}", response_model=schemas.CompeticionInDB)
def read_competicion(competicion_id: int, db: Session = Depends(get_db)):
    return crud.get_competicion_by_id(db, competicion_id)


# Crear una nueva competición
@app.post("/competiciones/", response_model=schemas.CompeticionInDB)
def create_new_competicion(competicion: schemas.CompeticionCreate, db: Session = Depends(get_db)):
    return crud.create_competicion(db, competicion)


# Eliminar una competición por ID
@app.delete("/competiciones/{competicion_id}")
def delete_competicion(competicion_id: int, db: Session = Depends(get_db)):
    return crud.delete_competicion_by_id(db, competicion_id)


@app.post("/resultados/", response_model=schemas.ResultadosInDB)
def create_resultado(resultado: schemas.ResultadosCreate, db: Session = Depends(get_db)):
    return crud.create_resultado(db, resultado)


@app.delete("/resultados/{resultado_id}", response_model=schemas.ResultadosInDB)
def delete_resultado(resultado_id: int, db: Session = Depends(get_db)):
    db_resultado = crud.delete_resultado(db, resultado_id)
    if db_resultado is None:
        raise HTTPException(status_code=404, detail="Resultado no encontrado")
    return db_resultado


@app.get("/resultados/", response_model=List[schemas.ResultadosInDB])
def get_all_resultados(db: Session = Depends(get_db)):
    return crud.get_all_resultados(db)


@app.get("/resultados/artista/{artista_id}", response_model=List[schemas.ResultadosInDB])
def get_resultados_by_artista(artista_id: int, db: Session = Depends(get_db)):
    resultados = crud.get_resultados_by_artista(db, artista_id)
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron resultados para este artista")
    return resultados


@app.get("/resultados/competicion/{competicion_id}", response_model=List[schemas.ResultadosInDB])
def get_resultados_by_competicion(competicion_id: int, db: Session = Depends(get_db)):
    resultados = crud.get_resultados_by_competicion(db, competicion_id)
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron resultados para esta competición")
    return resultados


@app.get("/resultados/puesto/{puesto}", response_model=List[schemas.ResultadosInDB])
def get_resultados_by_puesto(puesto: int, db: Session = Depends(get_db)):
    resultados = crud.get_resultados_by_puesto(db, puesto)
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron resultados con este puesto")
    return resultados


#
#
# TODO MONGO DB
#
#


@app.post("/insertar/")
def insertar_diccionario(diccionario: DiccionarioInsertar):
    try:
        # Convertir el modelo Pydantic a un diccionario
        data = diccionario.dict()

        # Insertar el diccionario en la colección
        result = chats.insert_one(data)

        return {"message": "Diccionario insertado", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agregar-mensaje/{diccionario_id}")
def agregar_mensaje(diccionario_id: str, mensaje: Mensaje):
    try:
        # Convertir el modelo Pydantic a un diccionario
        mensaje_dict = mensaje.dict()

        # Actualizar el documento para agregar el nuevo mensaje
        result = chats.update_one(
            {"_id": pymongo.ObjectId(diccionario_id)},
            {"$push": {"mensajes": mensaje_dict}}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Diccionario no encontrado")

        return {"message": "Mensaje agregado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chat/{diccionario_id}", response_model=DiccionarioInsertar)
def obtener_chat(diccionario_id: str):
    try:
        # Buscar el documento en la colección por su ID
        diccionario = chats.find_one({"_id": pymongo.ObjectId(diccionario_id)})

        if diccionario is None:
            raise HTTPException(status_code=404, detail="Diccionario no encontrado")

        # Convertir el ObjectId a string para la respuesta
        diccionario["_id"] = str(diccionario["_id"])

        return diccionario
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chat/maestro/{maestro_id}", response_model=List[DiccionarioInsertar])
def obtener_chat_por_maestro(maestro_id: int):
    try:
        # Buscar todos los documentos con el maestro_id dado
        chatEND = chats.find({"maestro_id": maestro_id})

        # Convertir los resultados a una lista
        result = []
        for chat in chatEND:
            chat["_id"] = str(chat["_id"])  # Convertir ObjectId a string
            result.append(chat)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Nuevo endpoint para buscar chat por aprendiz_id
@app.get("/chat/aprendiz/{aprendiz_id}", response_model=List[DiccionarioInsertar])
def obtener_chat_por_aprendiz(aprendiz_id: int):
    try:
        # Buscar todos los documentos con el aprendiz_id dado
        chatEND = chats.find({"aprendiz_id": aprendiz_id})

        # Convertir los resultados a una lista
        result = []
        for chat in chatEND:
            chat["_id"] = str(chat["_id"])  # Convertir ObjectId a string
            result.append(chat)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/eliminar-mensaje/{diccionario_id}/{timestamp}")
def eliminar_mensaje(diccionario_id: str, timestamp: datetime):
    try:
        # Actualizar el documento para eliminar el mensaje con el timestamp dado
        result = chats.update_one(
            {"_id": pymongo.ObjectId(diccionario_id)},
            {"$pull": {"mensajes": {"timestamp": timestamp}}}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Diccionario no encontrado o mensaje no encontrado")

        return {"message": "Mensaje eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/eliminar-chat/{diccionario_id}")
def eliminar_chat(diccionario_id: str):
    try:
        # Eliminar el documento del chat correspondiente al diccionario_id
        result = chats.delete_one({"_id": pymongo.ObjectId(diccionario_id)})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Chat no encontrado")

        return {"message": "Chat eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
