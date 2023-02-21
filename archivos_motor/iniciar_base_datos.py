import pymongo

#Referencia a mongoDB
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

#Crear la base de datos
database = mongo_client["motor-db"]

#Crear la colección
collection = database["motor"]

#Verificar si el registro ya existe
item_count = collection.count_documents({"_id": "https://www.elsoldemorelia.com.mx/" })

#Si el documento no existe, lo registramos
if item_count < 1:
    print("Creando nuevo documento")
    data = { 
            "_id": "https://www.elsoldemorelia.com.mx/", 
            "url": "https://www.elsoldemorelia.com.mx/",
            "revisado": False, 
            "palabra1": "",
            "ranking1": 0,
            "palabra2": "",
            "ranking2": 0,
            "palabra3": "",
            "ranking3": 0,
            "contenido": "" 
    }

    x = collection.insert_one(data)
else:
    print("El documento ya existe")