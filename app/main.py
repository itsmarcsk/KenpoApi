from datetime import datetime
from io import BytesIO
from typing import List

import gridfs
import pymongo
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from starlette.responses import JSONResponse

from BBDD.mongodb.database import chats, tienda_materialdb, material_collection, cesta, myclient, eventos, \
    tecnicas_katasdb, katas, tecnicas, eventosdb, fs_imagenes
from BBDD.mongodb.schemas import DiccionarioInsertar, Mensaje, CestaItem, MaterialItem, EventoInDB, EventoCreate, \
    MaterialInDB, MaterialCreate, KataInDB, TecnicaResponse
from BBDD.mysql import schemas, crud

from BBDD.mysql.crud import get_artista_marcial_by_dni, artista_marcial_exists, create_artista_marcial, \
    get_all_escuelas, get_escuela_by_id, create_escuela, delete_artista_marcial_by_dni, delete_escuela_by_id, \
    update_password_by_dni
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


# # Eliminar artista por ID
# @app.delete("/artistas-marciales/id/{artista_id}")
# def delete_artista_marcial_id(artista_id: int, db: Session = Depends(get_db)):
#     # Eliminar: Eliminar un artista marcial por su ID
#     return delete_artista_marcial_by_id(db, artista_id)


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

# TODO CHAT
# TODO FUNCIONA
@app.post("/chat/insertar/")
def insertar_diccionario(diccionario: DiccionarioInsertar):
    try:
        # Convertir el modelo Pydantic a un diccionario
        data = diccionario.dict()

        # Insertar el diccionario en la colección
        result = chats.insert_one(data)

        return {"message": "Diccionario insertado", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# TODO FUNCIONA
@app.post("/chat/agregar-mensaje/{diccionario_id}")
def agregar_mensaje(diccionario_id: str, mensaje: Mensaje):
    # Verificar que el ID del diccionario es válido
    if not ObjectId.is_valid(diccionario_id):
        raise HTTPException(status_code=400, detail="ID de diccionario inválido")

    try:
        # Convertir el modelo Pydantic a un diccionario
        mensaje_dict = mensaje.dict()

        # Actualizar el documento para agregar el nuevo mensaje
        result = chats.update_one(
            {"_id": ObjectId(diccionario_id)},
            {"$push": {"mensajes": mensaje_dict}}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Diccionario no encontrado")

        return {"message": "Mensaje agregado correctamente"}
    except Exception as e:
        print(f"Error al agregar el mensaje: {str(e)}")  # Para depuración
        raise HTTPException(status_code=500, detail="Error interno del servidor")


# TODO FUNCIONA
@app.get("/chat/{diccionario_id}", response_model=DiccionarioInsertar)
def obtener_chat(diccionario_id: str):
    try:
        # Buscar el documento en la colección por su ID
        diccionario = chats.find_one({"_id": ObjectId(diccionario_id)})

        if diccionario is None:
            raise HTTPException(status_code=404, detail="Diccionario no encontrado")

        # Convertir el ObjectId a string para la respuesta
        diccionario["_id"] = str(diccionario["_id"])

        return diccionario
    except Exception as e:
        # Imprimir el error en la consola para depuración
        print(f"Error al obtener el chat: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


# TODO FUNCIONA
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


# TODO FUNCIONA
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


# TODO FUNCIONA
@app.delete("/chat/eliminar-mensaje/{diccionario_id}/{timestamp}")
def eliminar_mensaje(diccionario_id: str, timestamp: str):
    try:
        # Convertir el timestamp a un objeto datetime
        timestamp_dt = datetime.fromisoformat(timestamp)  # Suponiendo que el formato sea 'YYYY-MM-DDTHH:MM:SS'

        print(f"Intentando eliminar el mensaje con timestamp: {timestamp_dt} del diccionario: {diccionario_id}")

        # Actualizar el documento para eliminar el mensaje con el timestamp dado
        result = chats.update_one(
            {"_id": ObjectId(diccionario_id)},
            {"$pull": {"mensajes": {"timestamp": timestamp_dt}}}
        )

        if result.matched_count == 0:
            print("No se encontró el diccionario o el mensaje.")
            raise HTTPException(status_code=404, detail="Diccionario no encontrado o mensaje no encontrado")

        print("Mensaje eliminado correctamente.")
        return {"message": "Mensaje eliminado correctamente"}

    except ValueError as ve:
        print(f"Error de formato de timestamp: {ve}")
        raise HTTPException(status_code=400, detail="Formato de timestamp inválido. Usa 'YYYY-MM-DDTHH:MM:SS'.")

    except Exception as e:
        print(f"Error inesperado: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# TODO FUNCIONA
@app.delete("/chat/eliminar-chat/{chat_id}")
async def eliminar_chat(chat_id: str):
    # Verificar si el ID proporcionado es un ObjectId válido
    if not ObjectId.is_valid(chat_id):
        raise HTTPException(status_code=400, detail="ID de chat inválido")

    # Intentar eliminar el chat
    result = chats.delete_one({"_id": ObjectId(chat_id)})

    # Verificar si se eliminó algún documento
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Chat no encontrado")

    return {"message": "Chat eliminado con éxito"}


# TODO EVENTOS


def get_eventos_collection():
    return eventos


# TODO FUNCIONA
@app.get("/eventos/")
async def get_eventos():
    try:
        eventos = list(eventosdb.eventos.find())
        eventos = [convert_objectid_to_str(evento) for evento in eventos]
        return JSONResponse(content={"eventos": eventos})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener eventos: {str(e)}")


# TODO FUNCIONA
@app.post("/eventos/")
async def create_evento(
        titulo: str = Form(...),
        descripcion: str = Form(...),
        fecha: str = Form(...),
        lugar: str = Form(...),
        imagen: UploadFile = File(...)
):
    # Verificar el tipo de imagen
    if imagen.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Formato de imagen no válido")

    # Leer el contenido de la imagen
    image_content = await imagen.read()

    # Guardar la imagen en GridFS usando GridFSBucket
    file_id = fs_imagenes.upload_from_stream(imagen.filename, image_content,
                                             metadata={"contentType": imagen.content_type})

    # Guardar los detalles del evento en la base de datos
    evento = {
        "titulo": titulo,
        "descripcion": descripcion,
        "fecha": fecha,
        "lugar": lugar,
        "id_imagen": str(file_id)  # Convertir ObjectId a cadena
    }

    # Insertar el evento en la base de datos
    eventosdb.eventos.insert_one(evento)

    # Convertir ObjectId del evento a cadena si es necesario
    if isinstance(evento["_id"], ObjectId):
        evento["_id"] = str(evento["_id"])

    return JSONResponse(content={"message": "Evento creado con éxito", "evento": evento})


# Función para convertir ObjectId a str
def convert_objectid_to_str(event):
    event["_id"] = str(event["_id"])  # Convertir _id a str
    return event


# TODO FUNCIONA
@app.get("/eventos/{evento_id}", response_model=EventoInDB)
async def get_evento(evento_id: str, db=Depends(get_eventos_collection)):
    if not ObjectId.is_valid(evento_id):
        raise HTTPException(status_code=400, detail="ID de evento inválido")

    evento = db.find_one({"_id": ObjectId(evento_id)})

    if evento is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    return EventoInDB(
        id=str(evento["_id"]),
        titulo=evento["titulo"],
        descripcion=evento["descripcion"],
        fecha=evento["fecha"],
        lugar=evento["lugar"],
        id_imagen=evento["id_imagen"]
    )


# TODO FUNCIONA
@app.delete("/eventos/{evento_id}")
async def eliminar_evento(evento_id: str):
    # Verificar que el ID sea válido
    try:
        evento_obj_id = ObjectId(evento_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID de evento no válido")

    # Buscar el evento en la base de datos
    evento = eventosdb.eventos.find_one({"_id": evento_obj_id})
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    # Eliminar la imagen de GridFS si existe
    if "id_imagen" in evento:
        imagen_id = evento["id_imagen"]
        try:
            # Convertir a ObjectId antes de eliminar
            imagen_obj_id = ObjectId(imagen_id)
            fs_imagenes.delete(imagen_obj_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="ID de imagen no válido")

    # Eliminar el evento de la colección
    resultado = eventosdb.eventos.delete_one({"_id": evento_obj_id})

    if resultado.deleted_count == 1:
        return {"message": "Evento y su imagen (si existía) eliminados con éxito"}
    else:
        raise HTTPException(status_code=500, detail="Error al eliminar el evento")


# TODO MATERIAL

def get_material_collection():
    return material_collection


@app.get("/materiales/")
async def get_materiales():
    try:
        materiales = list(tienda_materialdb.materiales.find())
        # Convertir ObjectId a string
        materiales = [convert_objectid_to_str(material) for material in materiales]
        return JSONResponse(content={"materiales": materiales})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener materiales: {str(e)}")


@app.post("/material/")
async def create_material(
        nombre: str = Form(...),
        descripcion: str = Form(...),
        precio: float = Form(...),
        imagen: UploadFile = File(...)
):
    # Verificar el tipo de imagen
    if imagen.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Formato de imagen no válido")

    # Leer el contenido de la imagen
    image_content = await imagen.read()

    # Guardar la imagen en GridFS usando GridFSBucket
    file_id = fs_imagenes.upload_from_stream(imagen.filename, image_content,
                                             metadata={"contentType": imagen.content_type})

    # Guardar los detalles del material en la base de datos
    material = {
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": precio,
        "id_imagen": str(file_id)  # Convertir ObjectId a cadena
    }

    # Insertar el material en la base de datos
    material_collection.materials.insert_one(material)  # Cambia esto por tu colección de materiales

    # Convertir ObjectId del material a cadena si es necesario
    if "_id" in material:
        material["_id"] = str(material["_id"])

    return JSONResponse(content={"message": "Material creado con éxito", "material": material})


@app.get("/material/{material_id}", response_model=MaterialInDB)
async def get_material(material_id: str, db=Depends(get_material_collection)):
    if not ObjectId.is_valid(material_id):
        raise HTTPException(status_code=400, detail="ID de material inválido")

    material = db.find_one({"_id": ObjectId(material_id)})

    if material is None:
        raise HTTPException(status_code=404, detail="Material no encontrado")

    return MaterialInDB(
        id=str(material["_id"]),
        nombre=material["nombre"],
        descripcion=material["descripcion"],
        precio=material["precio"],
        id_imagen=material["id_imagen"]
    )


@app.delete("/material/{material_id}")
async def eliminar_material(material_id: str):
    # Verificar que el ID sea válido
    try:
        material_obj_id = ObjectId(material_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID de material no válido")

    # Buscar el material en la base de datos
    material = material_collection.find_one({"_id": material_obj_id})
    if not material:
        raise HTTPException(status_code=404, detail="Material no encontrado")

    # Eliminar la imagen de GridFS si existe
    if "id_imagen" in material:
        imagen_id = material["id_imagen"]
        try:
            # Convertir a ObjectId antes de eliminar
            imagen_obj_id = ObjectId(imagen_id)
            fs_imagenes.delete(imagen_obj_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="ID de imagen no válido")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al eliminar la imagen: {str(e)}")

    # Eliminar el material de la base de datos
    material_collection.delete_one({"_id": material_obj_id})

    return {"message": "Material eliminado correctamente"}


# TODO CESTA
@app.get("/cesta/", response_model=List[dict])
def get_all_cesta_items():
    try:
        # Obtener todos los documentos de la colección 'cesta'
        items = list(cesta.find({}, {"_id": 0}))  # Excluyendo el _id de la respuesta

        if not items:
            raise HTTPException(status_code=404, detail="No se encontraron elementos en la colección")

        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los datos: {e}")


@app.get("/cesta/{artista_marcial_id}")
def get_material_by_artista_marcial(artista_marcial_id: int):
    # Busca el documento que coincide con el artista_marcial_id
    resultado = cesta.find_one({"artista_marcial_id": artista_marcial_id})

    if resultado is None:
        raise HTTPException(status_code=404, detail="Artista marcial no encontrado en la cesta")

    # Retorna la lista de material_id si se encuentra
    return {"artista_marcial_id": artista_marcial_id, "material_id": resultado.get("material_id", [])}


# Endpoint para añadir un nuevo item a la cesta
@app.post("/cesta/")
def add_to_cesta(item: CestaItem):
    try:
        # Convertir el item a un diccionario para MongoDB
        item_dict = item.dict()
        result = cesta.insert_one(item_dict)
        return {"message": "Item añadido a la cesta", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al añadir el item: {e}")


@app.put("/cesta/{artista_marcial_id}/add-material")
def add_material_to_cesta(artista_marcial_id: int, material_item: MaterialItem):
    try:
        # Buscar el documento con el artista_marcial_id
        result = cesta.update_one(
            {"artista_marcial_id": artista_marcial_id},  # Filtro para encontrar el documento
            {"$addToSet": {"material_id": material_item.material_id}}  # Añadir material_id sin duplicados
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Artista marcial no encontrado en la cesta")

        return {"message": "Material añadido correctamente al artista marcial"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al añadir el material: {e}")


@app.delete("/cesta/{artista_marcial_id}")
def delete_material_by_artista_marcial(artista_marcial_id: int):
    # Elimina todos los documentos que coinciden con el artista_marcial_id
    resultado = cesta.delete_many({"artista_marcial_id": artista_marcial_id})

    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="No se encontró ningún registro para el artista marcial")

    return {
        "message": f"Se eliminaron {resultado.deleted_count} registros para el artista_marcial_id {artista_marcial_id}"}


@app.delete("/cesta/material/{artista_marcial_id}")
def delete_material_list_by_artista_marcial(artista_marcial_id: int):
    # Elimina la lista de material_id para el artista_marcial_id dado
    resultado = cesta.update_one(
        {"artista_marcial_id": artista_marcial_id},  # Filtro para encontrar el documento
        {"$unset": {"material_id": ""}}  # Operador $unset para eliminar el campo material_id
    )

    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="No se encontró ningún registro para el artista marcial")

    return {"message": f"Se eliminó la lista de material_id para el artista_marcial_id {artista_marcial_id}"}


@app.delete("/cesta/material/{artista_marcial_id}/{material_id}")
def delete_material_from_list(artista_marcial_id: int, material_id: int):
    # Eliminar un material_id específico de la lista para un artista_marcial_id dado
    resultado = cesta.update_one(
        {"artista_marcial_id": artista_marcial_id},  # Filtro para encontrar el documento
        {"$pull": {"material_id": material_id}}  # Operador $pull para eliminar el elemento de la lista
    )

    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="No se encontró ningún registro para el artista marcial")

    if resultado.modified_count == 0:
        raise HTTPException(status_code=400, detail=f"No se encontró el material_id {material_id} en la lista")

    return {
        "message": f"El material_id {material_id} fue eliminado de la lista para el artista_marcial_id {artista_marcial_id}"}


@app.delete("/cesta/material/{material_id}")
def delete_material_from_all(material_id: int):
    # Eliminar un material_id específico de todas las listas en la colección
    resultado = cesta.update_many(
        {},  # Sin filtro, para afectar todos los documentos
        {"$pull": {"material_id": material_id}}  # Operador $pull para eliminar el material_id de todas las listas
    )

    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="No se encontraron registros con material_id en las listas")

    if resultado.modified_count == 0:
        raise HTTPException(status_code=400, detail=f"No se encontró el material_id {material_id} en ninguna lista")

    return {"message": f"El material_id {material_id} fue eliminado de todas las listas"}


# TODO FUNCIONA
@app.get("/imagenes/{imagen_id}")
async def get_imagen(imagen_id: str):
    if not ObjectId.is_valid(imagen_id):
        raise HTTPException(status_code=400, detail="ID de imagen inválido")

    try:
        # Obtener la imagen de GridFS utilizando open_download_stream
        imagen_data = fs_imagenes.open_download_stream(ObjectId(imagen_id))

        # Crear un flujo de bytes a partir de la imagen
        image_stream = BytesIO(imagen_data.read())

        # Registrar información para depuración
        print(
            f"Imagen encontrada: {imagen_id}, tamaño: {imagen_data.length} bytes, tipo: {imagen_data.metadata['contentType']}")

        return StreamingResponse(image_stream, media_type=imagen_data.metadata['contentType'])

    except gridfs.errors.NoFile:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    except Exception as e:
        # Capturamos y mostramos el error
        print(f"Error al obtener la imagen: {str(e)}")  # Registro de depuración
        raise HTTPException(status_code=500, detail=f"Error al obtener la imagen: {str(e)}")
