# Esquemas bases de datos

Los modelos son:

- Artistas marciales
- Escuelas
- Competiciones
- Resultados de las competiciones
- Chats
- Eventos
- Tecnicas
- Katas
- Materiales
- Cesta

Siendo los cuatro primeros para la base de datos mysql y los siguientes para la base de datos mongodb.


Los esquemas son los siguientes:

- Artista marcial

```python
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
```

- Escuela

```python
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
```

- Competiciones

```python
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
```

- Resultados competiciones

```python
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
```

- Mensaje(este se usa en chat)

```python
class Mensaje(BaseModel):
    autor_id: int
    contenido: str
    timestamp: datetime
```

- Diccionario(se usa para guardar el chat por completo)

```python
class DiccionarioInsertar(BaseModel):
    _id: str
    maestro_id: int
    aprendiz_id: int
    mensajes: List[Mensaje]
```

- Cesta

```python
class CestaItem(BaseModel):
    artista_marcial_id: int
    material_id: List[str]  # Lista de IDs de materiales


class MaterialItem(BaseModel):
    material_id: int  # El nuevo material que se va a añadir
```

- Material

```python
class MaterialBase(BaseModel):
    nombre: str
    descripcion: str
    precio: float


class MaterialCreate(MaterialBase):
    pass


class MaterialInDB(MaterialBase):
    id: str
    id_imagen: str

    class Config:
        from_attributes = True
```

- Eventos

```python
class EventoBase(BaseModel):
    titulo: str
    descripcion: str
    fecha: str
    lugar: str


class EventoCreate(EventoBase):
    id_imagen: str  # ID de la imagen almacenada en GridFS


class EventoInDB(EventoBase):
    id: str  # ID del evento en la base de datos
    id_imagen: str  # ID de la imagen almacenada en GridFS

    class Config:
        from_attributes = True
```

- Kata

```python
class KataCreate(BaseModel):
    nombre: str  # Nombre de la kata, requerido


class KataInDB(KataCreate):
    id: str
    id_video: str  # ID del video en GridFS

    class Config:
        from_attributes = True
```

- Técnica

```python
class TecnicaCreate(BaseModel):
    nombre: str  # Nombre de la técnica, requerido
    id_imagen: List[str]  # Lista de IDs de imágenes


class TecnicaInDB(TecnicaCreate):
    pass


class TecnicaResponse(BaseModel):
    id: str
    nombre: str
    id_imagen: List[str]

    class Config:
        from_attributes = True
```
