from sqlalchemy.orm import Session

from BBDD.mysql.schemas import ArtistaMarcialCreate
from models import ArtistaMarcial, Escuela, Competicion, ResultadoCompeticion
from BBDD.mysql import schemas, models


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
        contrasena=artista.contrasena  # Recuerda que la contraseña debe estar cifrada en un entorno de producción
    )

    # Añadimos el nuevo artista a la sesión de la base de datos
    db.add(db_artista)
    db.commit()  # Confirmamos la transacción
    db.refresh(db_artista)  # Refrescamos la instancia para obtener los datos actualizados

    return db_artista

