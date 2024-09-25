import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# TODO bases de datos
chatdb = myclient["chats"]
tecnicas_katasdb = myclient["tecnicas_katasdb"]
eventosdb = myclient["eventosdb"]
tienda_materialdb = myclient["tienda_materialdb"]

# TODO colecciones
chats = chatdb["chats"]

tecnicas = tecnicas_katasdb["tecnicas"]
katas = tecnicas_katasdb["katas"]

eventos = eventosdb["eventos"]

tienda_material = tienda_materialdb["tienda_material"]
cesta = tienda_materialdb["cesta"]

# TODO metodo de prueba para ver si se conecta print(myclient.list_database_names())
