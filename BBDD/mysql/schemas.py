from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from typing import List

from BBDD.mysql.models import ResultadoCompeticion


# TODO ARTISTA MARCIAL
class ArtistaMarcialBase(BaseModel):
    dni: str
    nombre: str
    apellidos: str
    fecha_nacimiento: str
    pais: str
    provincia: str
    comunidad_autonoma: str
    escuela_id: int
    cinturon: str
    grado: str
    contrasena: str | None = None  # contrasena es opcional

    class Config:
        orm_mode = True  # Cambiado de orm_mode a from_attributes


class ArtistaMarcialCreate(ArtistaMarcialBase):
    pass  # Todos los campos ya son requeridos


# Clase para la representación de Artistas Marciales en la base de datos
class ArtistaMarcialInDB(ArtistaMarcialBase):
    id: int  # ID existente

    class Config:
        orm_mode = True  # Permite la conversión de objetos ORM a diccionarios


# TODO ESCUELA

class EscuelaBase(BaseModel):
    nombre: str  # Requerido
    direccion: str  # Requerido
    ciudad: str  # Requerido
    pais: str  # Requerido


class EscuelaCreate(EscuelaBase):
    pass  # Todos los campos son requeridos al crear una nueva escuela


class EscuelaInDB(EscuelaBase):
    id: int  # ID existente

    class Config:
        orm_mode = True  # Permite la conversión de objetos ORM a diccionarios


# TODO COMPETICIONES


class CompeticionBase(BaseModel):
    nombre: str  # Requerido
    fecha: date  # Requerido
    lugar: str  # Requerido


class CompeticionCreate(CompeticionBase):
    pass  # Todos los campos son requeridos al crear una nueva competición


class CompeticionInDB(CompeticionBase):
    id: int  # ID existente
    resultados: List[ResultadoCompeticion] = []  # Relación opcional

    class Config:
        orm_mode = True  # Permite la conversión de objetos ORM a diccionarios
