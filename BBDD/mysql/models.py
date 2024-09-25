from sqlalchemy import Date, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from BBDD.mysql.database import Base


class ArtistaMarcial(Base):
    __tablename__ = 'artistas_marciales'

    id = Column(Integer, primary_key=True, autoincrement=True)  # ID existente
    dni = Column(String(9), nullable=False, unique=True)  # Nuevo campo dni
    nombre = Column(String(255), nullable=False)  # Campo requerido
    apellidos = Column(String(255), nullable=False)  # Campo requerido
    fecha_nacimiento = Column(Date, nullable=False)  # Campo requerido
    pais = Column(String(100), nullable=False)  # Campo requerido
    provincia = Column(String(100), nullable=False)  # Campo requerido
    comunidad_autonoma = Column(String(100), nullable=False)  # Campo requerido
    escuela_id = Column(Integer, nullable=False)  # Campo requerido
    cinturon = Column(String(50), nullable=False)  # Campo requerido
    grado = Column(String(50), nullable=False)  # Campo requerido
    contrasena = Column(String(255), nullable=True)  # Campo opcional


class Escuela(Base):
    __tablename__ = 'escuelas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)  # Requerido
    direccion = Column(String(255), nullable=False)  # Requerido
    ciudad = Column(String(100), nullable=False)  # Requerido
    pais = Column(String(100), nullable=False)  # Requerido


class Competicion(Base):
    __tablename__ = 'competiciones'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    fecha = Column(Date, nullable=False)
    lugar = Column(String(100), nullable=False)


class Resultados(Base):
    __tablename__ = 'resultados'

    id = Column(Integer, primary_key=True, autoincrement=True)
    artista_id = Column(Integer, nullable=False)  # Clave que ya no es foránea
    competicion_id = Column(Integer, nullable=False)  # Clave que ya no es foránea
    puesto = Column(Integer, nullable=False)  # Campo requerido
