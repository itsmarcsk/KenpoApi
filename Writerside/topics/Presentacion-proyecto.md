# Presentación del Proyecto

Este proyecto consiste en una API creada en Python utilizando la librería FastAPI. La API se comunica con una base de
datos MySQL y varias bases de datos MongoDB. Está diseñada con el objetivo de proporcionar a los artistas marciales
diversas funcionalidades a través de una página web.

## Funcionalidades principales:

- Visualización del progreso personal en las artes marciales.
- Compra de material relacionado con las artes marciales.
- Consulta de próximos eventos.
- Acceso a técnicas y katas.
- Comunicación directa con los maestros de su escuela.

Esta API ofrece una plataforma integrada para gestionar y visualizar el progreso en las artes marciales, facilitando la
interacción entre los artistas y sus maestros.

## Prerrequisitos para ejecución de api

Para poner en marcha la API, sigue los siguientes pasos:

### 1. Descargar Docker Desktop

Es necesario tener Docker Desktop instalado en tu máquina para poder gestionar las imágenes y los contenedores de
Docker.

### 2. Crear el contenedor de MySQL

Ejecuta el siguiente comando para crear el contenedor de MySQL:

```bash
docker run --name <nombre_contenedor> -e MYSQL_ROOT_PASSWORD=<contraseña> -e MYSQL_DATABASE=<nombre_base_de_datos> -p <puerto>:3306 -v <direccion_volumen>:/var/lib/mysql -d mysql:latest
```

- `docker run`: Inicia un contenedor nuevo a partir de una imagen de Docker.
- `--name`: Asigna un nombre al contenedor para referenciarlo más fácilmente.
- `-e MYSQL_ROOT_PASSWORD`: Define la contraseña del usuario root de MySQL.
- `-e MYSQL_DATABASE`: Crea automáticamente una base de datos al iniciar el contenedor.
- `-p <puerto>:3306`: Redirige el puerto 3306 (dentro del contenedor) al puerto de tu máquina host.
- `-v <direccion_volumen>:/var/lib/mysql`: Monta un volumen local para persistir los datos de MySQL.
- `-d`: Ejecuta el contenedor en segundo plano.
- `mysql:latest`: Utiliza la última versión disponible de la imagen oficial de MySQL.

### 3. Crear el contenedor de MongoDB

Ejecuta el siguiente comando para crear el contenedor de MongoDB:

```bash
docker run --name <nombre_contenedor> -d -p <puerto>:27017 -v <volumen>:/data/db mongo
```

### 4. Crear conexiones entre dockers

<h4>4.1. Crear conexión</h4>

```bash
docker network create <nombre_conexion>
```

<h4>4.2. Meter dockers en la conexion</h4>

```bash
docker network connect <nombre_conexion> <nombre_contenedor>
```

<h4>4.3. Fijarse en las direcciones</h4>

Una vez añadidos los dos contenedores a la conexión, hay que comprobar la dirección ip del contenedor de mysql para
ponerlo dentro del codigo de la api en el fichero `database.py`. Se encuentra:

```bash
BBDD/mysql/database.py
```

En este, habrá que poner la ip del contenedor mysql en la siguiente línea y en caso de que se haya puesto nombre de la
tfc, cambiarlo aquí también:

```python
SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://root:root@<ip_contenedor>:3306/<nombre_base_de_datos>"
```

Y habrá que hacer lo mismo con el de mongodb

```bash
BBDD/mongodb/database.py
```

Y habrá que ponerlo de la siguiente manera:

```python
myclient = pymongo.MongoClient("mongodb://<ip_contenedor>:27017/")
```

Para poder hacer esto, habrá que usar el comando:

```bash
docker network inspect <nombre_conexion>
```

Saldrá algo como esto:

```bash
[
    {
        "Name": "my_network",
        "Id": "028353b6f271f65578fc5c0d943fb45e364b3f2bd5de509435a341f52cede523",
        "Created": "2024-09-27T09:49:32.287605912Z",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.18.0.0/16",
                    "Gateway": "172.18.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "ced8fdf8a2299db91e0b5c5cbdbad858e47c3e0ef05e5e789b39fbb81f910587": {
                "Name": "mysql_container",
                "EndpointID": "e3d5e47beddf71c101dc41e7d806243d57a2d4012fba2614a93ce0d449d607d4",
                "MacAddress": "02:42:ac:12:00:03",
                "IPv4Address": "172.18.0.3/16",
                "IPv6Address": ""
            },
            "ec59ea9221a5ea8df205fa1587acbb97c72b94fa18bf816253f1783fe1a443c9": {
                "Name": "mongo-container",
                "EndpointID": "40d1cba96a24a76b4fdb3fd6767f508b8d2f3f9647274b1a2b964ecdb8014548",
                "MacAddress": "02:42:ac:12:00:02",
                "IPv4Address": "172.18.0.2/16",
                "IPv6Address": ""
            }
        },
        "Options": {},
        "Labels": {}
    }
]
```

Habrá que fijarse dentro de `Containers` y dentro de containers el que tiene en `Name` el nombre elegido para el
contenedor de mysql y en él habrá que mirar su `IPv4Address` ya que habrá que copiarla donde se ha indicado
anteriormente, sin añadir lo que viene tras el `/`

## Instalación y funcionamiento de api

### 1. Crear la imagen de Docker

Dentro del proyecto, usa el siguiente comando para crear la imagen a partir del Dockerfile:

```bash
docker build -t <nombre_imagen> .
```

> **Nota**: No se debe mover nada del proyecto ya que está preparado para que todo funcione en la dirección establecida
> en el Dockerfile.

Una vez creada la imagen, habrá que crear el contenedor de la api a partir del siguiente comando que utilizará la imagen
que creamos

```bash
docker run -d --name <nombre_contenedor> -p 80:80 <nombre_imagen>
```

### 2. Crear contenedor de API

docker run: Comando base que indica que quieres ejecutar un nuevo contenedor.

`-d`: Ejecuta el contenedor en modo "detached", es decir, en segundo plano, sin bloquear la terminal.

`--name` : Asigna un nombre al contenedor para que puedas referenciarlo fácilmente. Debes reemplazar <nombre_contenedor>
por el nombre que desees (ej. mi_contenedor).

`-p 80:80`: Redirige el puerto 80 del contenedor al puerto 80 de tu máquina host. Esto te permite acceder al servicio
que se esté ejecutando dentro del contenedor (por ejemplo, un servidor web) desde tu máquina local a través del puerto
`80`.

> Al crear el contenedor, veremos que da error y se dejará de ejecutar, por lo que habrá que añadirla a la conexion en
> el que están los contenedores de las bases de datos

```bash
docker network connect <nombre_conexion> <nombre_contenedor>
```

Volvemos a ejecutar la API y veremos que ahora no debería de dar errores

```bash
docker exec -it <nombre_contenedor>
```