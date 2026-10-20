from pymongo import MongoClient
from pymongo .errors import ConnectionFailure, ServerSelectionTimeoutError

#agregar la URI de conexión a la base de datos MongoDB
MONGO_URI = "mongodb+srv://johndaviddiax_db_user:1013345649Xx@cluster0.864ytp1.mongodb.net/?appName=Cluster0"

#crear una instancia swl cliente de mongodb y asignar un tiempo de espera para la seccion del servidor
client= MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)

#crerar la bd y la coleccion
db = client.dataAP
collection = db.trainee

try:
    #verificar la conexión al servidor de mongodb
    client.server_info()
    client.admin.command('ping')
    print("Conexión exitosa a MongoDB")
except (ConnectionFailure, ServerSelectionTimeoutError) as e:
    print(f"Error de conexión a MongoDB: {e}")
    