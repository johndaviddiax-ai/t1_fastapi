from pymongo import MongoClient
from pymongo .errors import ConnectionFailure, ServerSelectionTimeoutError

#agregar la URI de conexión a la base de datos MongoDB
MONGO_URI = "mongodb+srv://johndaviddiax_db_user:1013345649Xx@cluster0.864ytp1.mongodb.net/?appName=Cluster0"

#crear una instancia swl cliente de mongodb y asignar un tiempo de espera para la seccion del servidor
client= MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)

#crerar la bd y la coleccion
db = client.ambiente703
collection = db.mesa

#crear el modelo de datos para la colecion
nuevaMesa ={
    "name": "John Diaz",
    "status": "Alive",
    "species": "Human",
    "gender": "Male"
}

#insertar el modelo de datos en la coleccion
collection.insert_one(nuevaMesa)
print("Documento insertado en la colección 'mesa' de la base de datos 'ambiente703'")

try:
    #verificar la conexión al servidor de mongodb
    client.server_info()
    client.admin.command('ping')
    print("Conexión exitosa a MongoDB")
except (ConnectionFailure, ServerSelectionTimeoutError) as e:
    print(f"Error de conexión a MongoDB: {e}")
    
finally:
    #cerrar la conexión al servidor de mongodb
    client.close()