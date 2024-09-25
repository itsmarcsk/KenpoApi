from fastapi import HTTPException
from sqlalchemy.orm import Session

from BBDD.mysql.schemas import ArtistaMarcialCreate, EscuelaCreate
from tools.PasswordEncryptor import PasswordEncryptor
from .models import ArtistaMarcial, Escuela


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


def artista_marcial_exists(db: Session, dni: str) -> bool:
    """Verifica si un artista marcial existe por su DNI."""
    return db.query(ArtistaMarcial).filter(ArtistaMarcial.dni == dni).first() is not None


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
        contrasena=hashed_password
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
