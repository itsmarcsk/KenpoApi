from sqlalchemy import Date
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from BBDD.mysql.database import Base


class ArtistaMarcial(Base):
    __tablename__ = 'artistas_marciales'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=True)
    apellidos = Column(String(255), nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    pais = Column(String(100), nullable=True)
    provincia = Column(String(100), nullable=True)
    comunidad_autonoma = Column(String(100), nullable=True)
    escuela_id = Column(Integer, ForeignKey('escuelas.id'),
                        nullable=True)  # Cambia 'escuelas.id' por el nombre correcto de la tabla y columna de referencia
    cinturon = Column(String(50), nullable=True)
    grado = Column(String(50), nullable=True)
    contrasena = Column(String(255), nullable=True)

    # Relación con la tabla Escuela
    escuela = relationship("Escuela", back_populates="artistas_marciales")


class Escuela(Base):
    __tablename__ = 'escuelas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=True)
    direccion = Column(String(255), nullable=True)
    ciudad = Column(String(100), nullable=True)
    pais = Column(String(100), nullable=True)

    # Relación con la tabla ArtistaMarcial
    artistas_marciales = relationship("ArtistaMarcial", back_populates="escuela")


class Competicion(Base):
    __tablename__ = 'competiciones'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=True)
    fecha = Column(Date, nullable=True)
    lugar = Column(String(100), nullable=True)

    # Relación con la tabla ArtistaMarcial a través de una tabla intermedia si es necesario
    artistas_marciales = relationship("ArtistaMarcial", secondary="artista_competicion", back_populates="competiciones")


class ResultadoCompeticion(Base):
    __tablename__ = 'resultados_competiciones'

    id = Column(Integer, primary_key=True, autoincrement=True)
    artista_id = Column(Integer, ForeignKey('artistas_marciales.id'), nullable=True)
    competicion_id = Column(Integer, ForeignKey('competiciones.id'), nullable=True)
    puesto = Column(Integer, nullable=True)

    # Relaciones con las tablas ArtistaMarcial y Competicion
    artista = relationship("ArtistaMarcial", back_populates="resultados")
    competicion = relationship("Competicion", back_populates="resultados")
