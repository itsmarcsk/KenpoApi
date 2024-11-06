from fastapi import HTTPException
from sqlalchemy.orm import Session

from BBDD.mysql.schemas import ArtistaMarcialCreate, EscuelaCreate, CompeticionCreate
from tools.PasswordEncryptor import PasswordEncryptor
from . import models, schemas
from .models import ArtistaMarcial, Escuela, Competicion


# TODO ARTISTAS MARCIALES

def get_artista_marcial_by_dni(db: Session, dni: str):
    """Obtiene un artista marcial por su DNI."""
    artista = db.query(ArtistaMarcial).filter(ArtistaMarcial.dni == dni).first()

    if not artista:
        return None

    return {
        "id": artista.id,
        "dni": artista.dni,
        "nombre": artista.nombre,
        "apellidos": artista.apellidos,
        "fecha_nacimiento": artista.fecha_nacimiento,
        "pais": artista.pais,
        "provincia": artista.provincia,
        "comunidad_autonoma": artista.comunidad_autonoma,
        "escuela_id": artista.escuela_id,
        "cinturon": artista.cinturon,
        "grado": artista.grado,
    }


def create_artista_marcial(db: Session, artista: ArtistaMarcialCreate):
    """Crea un nuevo artista marcial."""
    hashed_password = PasswordEncryptor.hash_password(artista.contrasena)

    db_artista = ArtistaMarcial(
        dni=artista.dni,
        nombre=artista.nombre,
        apellidos=artista.apellidos,
        fecha_nacimiento=artista.fecha_nacimiento,
        pais=artista.pais,
        provincia=artista.provincia,
        comunidad_autonoma=artista.comunidad_autonoma,
        escuela_id=artista.escuela_id,
        cinturon=artista.cinturon,
        grado=artista.grado,
        contrasena=""
    )

    db.add(db_artista)
    db.commit()
    db.refresh(db_artista)

    return db_artista


def delete_artista_marcial_by_dni(db: Session, dni: str):
    """Elimina un artista marcial por su DNI."""
    artista = db.query(ArtistaMarcial).filter(ArtistaMarcial.dni == dni).first()

    if not artista:
        raise HTTPException(status_code=404, detail="Artista marcial no encontrado")

    db.delete(artista)
    db.commit()
    return {"detail": "Artista marcial eliminado exitosamente"}


def delete_artista_marcial_by_id(db: Session, artista_id: int):
    """Elimina un artista marcial por su ID."""
    artista = db.query(ArtistaMarcial).filter(ArtistaMarcial.id == artista_id).first()

    if not artista:
        raise HTTPException(status_code=404, detail="Artista marcial no encontrado")

    db.delete(artista)
    db.commit()
    return {"detail": "Artista marcial eliminado exitosamente"}


def update_password_by_dni(db: Session, dni: str, new_password: str):
    """Actualiza la contraseña de un artista marcial por su DNI."""
    artista = db.query(ArtistaMarcial).filter(ArtistaMarcial.dni == dni).first()

    if not artista:
        raise HTTPException(status_code=404, detail="Artista marcial no encontrado")

    hashed_password = PasswordEncryptor.hash_password(new_password)
    artista.contrasena = hashed_password

    db.commit()
    db.refresh(artista)

    return artista


# TODO ESCUELA

def get_all_escuelas(db: Session):
    """Obtiene todas las escuelas."""
    return db.query(Escuela).all()


def get_escuela_by_id(db: Session, escuela_id: int):
    """Obtiene una escuela por su ID."""
    return db.query(Escuela).filter(Escuela.id == escuela_id).first()


def create_escuela(db: Session, escuela: EscuelaCreate):
    """Crea una nueva escuela."""
    nueva_escuela = Escuela(
        nombre=escuela.nombre,
        direccion=escuela.direccion,
        ciudad=escuela.ciudad,
        pais=escuela.pais
    )

    db.add(nueva_escuela)
    db.commit()
    db.refresh(nueva_escuela)

    return nueva_escuela


def delete_escuela_by_id(db: Session, escuela_id: int):
    """Elimina una escuela por su ID."""
    escuela = db.query(Escuela).filter(Escuela.id == escuela_id).first()

    if not escuela:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")

    db.delete(escuela)
    db.commit()
    return {"detail": "Escuela eliminada exitosamente"}


# TODO COMPETICIONES

# Obtener todas las competiciones
def get_all_competiciones(db: Session):
    return db.query(Competicion).all()


# Obtener una competición por ID
def get_competicion_by_id(db: Session, competicion_id: int):
    competicion = db.query(Competicion).filter(Competicion.id == competicion_id).first()
    if not competicion:
        raise HTTPException(status_code=404, detail="Competición no encontrada")
    return competicion


# Crear una nueva competición
def create_competicion(db: Session, competicion: CompeticionCreate):
    db_competicion = Competicion(
        nombre=competicion.nombre,
        fecha=competicion.fecha,
        lugar=competicion.lugar
    )
    db.add(db_competicion)
    db.commit()  # Confirmar la transacción
    db.refresh(db_competicion)  # Refrescar la instancia para obtener los datos actualizados
    return db_competicion


# Eliminar una competición por ID
def delete_competicion_by_id(db: Session, competicion_id: int):
    competicion = db.query(Competicion).filter(Competicion.id == competicion_id).first()
    if not competicion:
        raise HTTPException(status_code=404, detail="Competición no encontrada")
    db.delete(competicion)
    db.commit()  # Confirmar la eliminación
    return {"detail": "Competición eliminada exitosamente"}


# TODO RESULTADOS
def create_resultado(db: Session, resultado: schemas.ResultadosCreate):
    db_resultado = models.Resultados(
        artista_id=resultado.artista_id,
        competicion_id=resultado.competicion_id,
        puesto=resultado.puesto
    )
    db.add(db_resultado)
    db.commit()
    db.refresh(db_resultado)
    return db_resultado


def delete_resultado(db: Session, resultado_id: int):
    db_resultado = db.query(models.Resultados).filter(models.Resultados.id == resultado_id).first()
    if db_resultado is None:
        raise HTTPException(status_code=404, detail="Resultado no encontrado")
    db.delete(db_resultado)
    db.commit()
    return {"detail": "Resultado eliminado exitosamente"}


def get_all_resultados(db: Session):
    return db.query(models.Resultados).all()


def get_resultados_by_artista(db: Session, artista_id: int):
    return db.query(models.Resultados).filter(models.Resultados.artista_id == artista_id).all()


def get_resultados_by_competicion(db: Session, competicion_id: int):
    return db.query(models.Resultados).filter(
        models.Resultados.competicion_id == competicion_id).all()


def get_resultados_by_puesto(db: Session, puesto: int):
    return db.query(models.Resultados).filter(models.Resultados.puesto == puesto).all()
