# Modelo de datos para el mensaje
from datetime import datetime, date
from typing import List

from pydantic import BaseModel


# TODO CHAT
class Mensaje(BaseModel):
    autor_id: int
    contenido: str
    timestamp: datetime


# Modelo de datos para el diccionario que se va a insertar
class DiccionarioInsertar(BaseModel):
    _id: str
    maestro_id: int
    aprendiz_id: int
    mensajes: List[Mensaje]


# Definir el modelo para un ítem de material con cantidad
class MaterialItem(BaseModel):
    material_id: str  # ID del material
    cantidad: int  # Cantidad del material


# Definir el modelo de CestaItem, que ahora tiene una lista de MaterialItems
class CestaItem(BaseModel):
    artista_marcial_id: str  # ID del artista marcial
    materiales: List[MaterialItem]  # Lista de materiales con ID y cantidad


class EventoBase(BaseModel):
    titulo: str
    descripcion: str
    fecha: str
    lugar: str


class EventoCreate(EventoBase):
    id_imagen: str  # ID de la imagen almacenada en GridFS


class EventoInDB(EventoBase):
    id: str  # ID del evento en la base de datos
    id_imagen: str  # ID de la imagen almacenada en GridFS

    class Config:
        from_attributes = True


class MaterialBase(BaseModel):
    nombre: str
    descripcion: str
    precio: float


class MaterialCreate(MaterialBase):
    pass


class MaterialInDB(MaterialBase):
    id: str
    id_imagen: str

    class Config:
        from_attributes = True


class KataCreate(BaseModel):
    nombre: str  # Nombre de la kata, requerido


class KataInDB(KataCreate):
    id: str
    id_video: str  # ID del video en GridFS

    class Config:
        from_attributes = True


class TecnicaCreate(BaseModel):
    nombre: str  # Nombre de la técnica, requerido
    id_imagen: str  # Lista de IDs de imágenes


class TecnicaInDB(TecnicaCreate):
    pass


class TecnicaResponse(BaseModel):
    id: str
    nombre: str
    id_imagen: str

    class Config:
        from_attributes = True
