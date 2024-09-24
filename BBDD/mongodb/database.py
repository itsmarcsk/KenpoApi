import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

chatdb = myclient["chatdb"]
tecnicas_katasdb = myclient["tecnicas_katasdb"]
eventosdb = myclient["eventosdb"]
tienda_materialdb = myclient["tienda_materialdb"]

chats = chatdb["chats"]
tecnicas = tecnicas_katasdb["tecnicas"]
katas = tecnicas_katasdb["katas"]
eventos = eventosdb["eventos"]
tienda_material = tienda_materialdb["tienda_material"]

#TODO metodo de prueba para ver si se conecta print(myclient.list_database_names())