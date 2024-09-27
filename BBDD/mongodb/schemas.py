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
    maestro_id: int
    aprendiz_id: int
    mensajes: List[Mensaje]


class CestaItem(BaseModel):
    artista_marcial_id: int
    material_id: List[int]  # Lista de IDs de materiales


class MaterialItem(BaseModel):
    material_id: int  # El nuevo material que se va a añadir


class EventoBase(BaseModel):
    titulo: str
    descripcion: str
    fecha: date
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
    id_video: str  # ID del video en GridFS

    class Config:
        from_attributes = True


class TecnicaCreate(BaseModel):
    nombre: str  # Nombre de la técnica, requerido
    id_imagen: List[str]  # Lista de IDs de imágenes


class TecnicaInDB(TecnicaCreate):
    pass


class TecnicaResponse(BaseModel):
    id: str
    nombre: str
    id_imagen: List[str]

    class Config:
        from_attributes = True
