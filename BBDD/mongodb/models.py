# Modelo de datos para el mensaje
from datetime import datetime
from typing import List

from pydantic import BaseModel


class Mensaje(BaseModel):
    autor_id: int
    contenido: str
    timestamp: datetime


# Modelo de datos para el diccionario que se va a insertar
class DiccionarioInsertar(BaseModel):
    maestro_id: int
    aprendiz_id: int
    mensajes: List[Mensaje]
