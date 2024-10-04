from pydantic import BaseModel
from datetime import date
from typing import Optional


# TODO ARTISTA MARCIAL
class ArtistaMarcialBase(BaseModel):
    dni: str  # Requerido
    nombre: str  # Requerido
    apellidos: str  # Requerido
    fecha_nacimiento: date  # Requerido
    pais: str  # Requerido
    provincia: str  # Requerido
    comunidad_autonoma: str  # Requerido
    escuela_id: int  # Requerido
    cinturon: str  # Requerido
    grado: str  # Requerido
    contrasena: Optional[str] = None  # Opcional


class ArtistaMarcialCreate(ArtistaMarcialBase):
    pass  # Todos los campos son requeridos al crear un nuevo artista marcial


class ArtistaMarcialInDB(ArtistaMarcialBase):
    id: int  # ID existente

    class Config:
        from_attributes = True  # Permite la conversión de objetos ORM a diccionarios


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
        from_attributes = True  # Permite la conversión de objetos ORM a diccionarios


# TODO COMPETICIONES
class CompeticionBase(BaseModel):
    nombre: str  # Requerido
    fecha: date  # Requerido
    lugar: str  # Requerido


class CompeticionCreate(CompeticionBase):
    pass  # Todos los campos son requeridos al crear una nueva competicion


class CompeticionInDB(CompeticionBase):
    id: int  # ID existente

    class Config:
        from_attributes = True  # Permite la conversión de objetos ORM a diccionarios


# TODO  RESULTADO COMPETICIONES
class ResultadosBase(BaseModel):
    artista_id: int  # Requerido
    competicion_id: int  # Requerido
    puesto: int  # Requerido


class ResultadosCreate(ResultadosBase):
    pass  # Todos los campos son requeridos al crear un nuevo resultado


class ResultadosInDB(ResultadosBase):
    id: int  # ID existente, asumiendo que el modelo Resultados tiene un campo id

    class Config:
        from_attributes = True  # Permite la conversión de objetos ORM a diccionarios
