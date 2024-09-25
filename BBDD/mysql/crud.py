from fastapi import HTTPException
from sqlalchemy.orm import Session

from BBDD.mysql.schemas import ArtistaMarcialCreate, EscuelaCreate
from tools.PasswordEncryptor import PasswordEncryptor
from .models import ArtistaMarcial, Escuela


# TODO ARTISTAS MARCIALES
def get_artista_marcial_by_dni(db: Session, dni: str):
    # Consulta para obtener el artista por su DNI
    artista = db.query(ArtistaMarcial).filter(ArtistaMarcial.dni == dni).first()

    # Si no se encuentra el artista, devolver None
    if not artista:
        return None

    # Retornar un diccionario con todos los campos menos la contraseña
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
    return db.query(ArtistaMarcial).filter(ArtistaMarcial.dni == dni).first() is not None


def create_artista_marcial(db: Session, artista: ArtistaMarcialCreate):
    # Hashear la contraseña
    hashed_password = PasswordEncryptor.hash_password(artista.contrasena)

    # Creamos una instancia del modelo ArtistaMarcial
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
        contrasena=hashed_password  # Guardamos la contraseña hasheada
    )

    # Añadimos el nuevo artista a la sesión de la base de datos
    db.add(db_artista)
    db.commit()  # Confirmamos la transacción
    db.refresh(db_artista)  # Refrescamos la instancia para obtener los datos actualizados

    return db_artista


def delete_artista_marcial_by_dni(db: Session, dni: str):
    # Buscar el artista por DNI
    artista = db.query(ArtistaMarcial).filter(ArtistaMarcial.dni == dni).first()

    # Si no se encuentra, lanzar una excepción
    if not artista:
        raise HTTPException(status_code=404, detail="Artista marcial no encontrado")

    # Eliminar el artista
    db.delete(artista)
    db.commit()  # Confirmar la eliminación
    return {"detail": "Artista marcial eliminado exitosamente"}


def delete_artista_marcial_by_id(db: Session, artista_id: int):
    # Buscar el artista por ID
    artista = db.query(ArtistaMarcial).filter(ArtistaMarcial.id == artista_id).first()

    # Si no se encuentra, lanzar una excepción
    if not artista:
        raise HTTPException(status_code=404, detail="Artista marcial no encontrado")

    # Eliminar el artista
    db.delete(artista)
    db.commit()  # Confirmar la eliminación
    return {"detail": "Artista marcial eliminado exitosamente"}


def update_password_by_dni(db: Session, dni: str, new_password: str):
    # Buscar el artista por su DNI
    artista = db.query(ArtistaMarcial).filter(ArtistaMarcial.dni == dni).first()

    if not artista:
        raise HTTPException(status_code=404, detail="Artista marcial no encontrado")

    # Encriptar la nueva contraseña
    hashed_password = PasswordEncryptor.hash_password(new_password)

    # Actualizar la contraseña
    artista.contrasena = hashed_password

    db.commit()  # Confirmamos los cambios
    db.refresh(artista)  # Refrescamos la instancia para obtener los datos actualizados

    return artista


# TODO ESCUELA

def get_all_escuelas(db: Session):
    # Consulta para obtener todas las escuelas
    return db.query(Escuela).all()


def get_escuela_by_id(db: Session, escuela_id: int):
    # Consulta para obtener una escuela por su ID
    return db.query(Escuela).filter(Escuela.id == escuela_id).first()


def create_escuela(db: Session, escuela: EscuelaCreate):
    # Crear una instancia de Escuela a partir del esquema recibido
    nueva_escuela = Escuela(
        nombre=escuela.nombre,
        direccion=escuela.direccion,
        ciudad=escuela.ciudad,
        pais=escuela.pais
    )

    # Añadir la nueva escuela a la base de datos
    db.add(nueva_escuela)
    db.commit()  # Confirmar los cambios
    db.refresh(nueva_escuela)  # Refrescar la instancia para obtener el ID generado

    return nueva_escuela


def delete_escuela_by_id(db: Session, escuela_id: int):
    # Buscar la escuela por ID
    escuela = db.query(Escuela).filter(Escuela.id == escuela_id).first()

    # Si no se encuentra, lanzar una excepción
    if not escuela:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")

    # Eliminar la escuela
    db.delete(escuela)
    db.commit()  # Confirmar la eliminación
    return {"detail": "Escuela eliminada exitosamente"}
