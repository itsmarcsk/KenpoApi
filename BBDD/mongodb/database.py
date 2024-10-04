import gridfs
import pymongo

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
myclient = pymongo.MongoClient("mongodb://172.18.0.2:27017/")

# TODO bases de datos
chatdb = myclient["chats"]
tecnicas_katasdb = myclient["tecnicas_katasdb"]
eventosdb = myclient["eventosdb"]
tienda_materialdb = myclient["tienda_materialdb"]

imagenes = myclient["imagenes"]
fs_imagenes = gridfs.GridFSBucket(imagenes)
videos = myclient["videos"]
fs_videos = gridfs.GridFSBucket(videos)

# TODO colecciones
chats = chatdb["chats"]

tecnicas = tecnicas_katasdb["tecnicas"]
katas = tecnicas_katasdb["katas"]

eventos = eventosdb["eventos"]

material_collection = tienda_materialdb["tienda_material"]
cesta = tienda_materialdb["cesta"]

# TODO metodo de prueba para ver si se conecta print(myclient.list_database_names())
