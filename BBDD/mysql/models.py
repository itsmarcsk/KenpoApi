from sqlalchemy import Date
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from BBDD.mysql.database import Base


class ArtistaMarcial(Base):
    __tablename__ = 'artistas_marciales'

    id = Column(Integer, primary_key=True, autoincrement=True)  # ID existente
    dni = Column(String(9), nullable=False)  # Nuevo campo dni
    nombre = Column(String(255), nullable=False)  # Campo requerido
    apellidos = Column(String(255), nullable=False)  # Campo requerido
    fecha_nacimiento = Column(Date, nullable=False)  # Campo requerido
    pais = Column(String(100), nullable=False)  # Campo requerido
    provincia = Column(String(100), nullable=False)  # Campo requerido
    comunidad_autonoma = Column(String(100), nullable=False)  # Campo requerido
    escuela_id = Column(Integer, ForeignKey('escuelas.id'), nullable=False)  # Campo requerido
    cinturon = Column(String(50), nullable=False)  # Campo requerido
    grado = Column(String(50), nullable=False)  # Campo requerido
    contrasena = Column(String(255), nullable=True)  # Campo opcional
    # Relación con la tabla Escuela
    escuela = relationship("Escuela", back_populates="artistas_marciales")
    resultados = relationship("ResultadoCompeticion", back_populates="artista")


class Escuela(Base):
    __tablename__ = 'escuelas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)  # Requerido
    direccion = Column(String(255), nullable=False)  # Requerido
    ciudad = Column(String(100), nullable=False)  # Requerido
    pais = Column(String(100), nullable=False)  # Requerido

    # Relación con la tabla ArtistaMarcial
    artistas_marciales = relationship("ArtistaMarcial", back_populates="escuela")


class Competicion(Base):
    __tablename__ = 'competiciones'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=True)
    fecha = Column(Date, nullable=True)
    lugar = Column(String(100), nullable=True)



class ResultadoCompeticion(Base):
    __tablename__ = 'resultados_competiciones'

    id = Column(Integer, primary_key=True, autoincrement=True)
    artista_id = Column(Integer, ForeignKey('artistas_marciales.id'), nullable=False)  # Clave foránea requerida
    competicion_id = Column(Integer, ForeignKey('competiciones.id'), nullable=False)  # Clave foránea requerida
    puesto = Column(Integer, nullable=True)  # Campo opcional

    # Relaciones con las tablas ArtistaMarcial y Competicion
    artista = relationship("ArtistaMarcial", back_populates="resultados")
    competicion = relationship("Competicion", back_populates="resultados")