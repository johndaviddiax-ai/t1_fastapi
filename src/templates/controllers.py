from bson import ObjectId
from src.models.database import collection
from src.models.model import TraineeModel, TraineeUpdateModel


def helper_trainee(trainee) -> dict:
    return {
        "id": str(trainee["_id"]),
        "document": trainee["document"],
        "firstname": trainee["firstname"],
        "lastname": trainee["lastname"],
        "email": trainee["email"],
        "age": trainee["age"],
        "program": trainee["program"],
        "record_number": trainee["record_number"],
    }


# Crear datos de un aprendiz
def create_trainee(trainee: TraineeModel):
    trainee_dict = trainee.model_dump()
    result = collection.insert_one(trainee_dict)
    new_trainee = collection.find_one({"_id": result.inserted_id})
    return helper_trainee(new_trainee)


# Buscar aprendiz por documento (para evitar duplicados)
def get_trainee_by_document(document):
    trainee = collection.find_one({"document": document})
    return helper_trainee(trainee) if trainee else None


# Obtener todos los aprendices
def get_all_trainees():
    return [helper_trainee(trainee) for trainee in collection.find()]


# Obtener datos del aprendiz por ID
def get_trainee_by_id(id: str):
    if not ObjectId.is_valid(id):
        return None
    trainee = collection.find_one({"_id": ObjectId(id)})
    return helper_trainee(trainee) if trainee else None


# Actualizar datos del aprendiz por ID
def update_trainee(id: str, data: TraineeUpdateModel):
    if not ObjectId.is_valid(id):
        return None

    data_update = data.model_dump(exclude_none=True)

    if data_update:
        collection.update_one({"_id": ObjectId(id)}, {"$set": data_update})

    trainee_updated = collection.find_one({"_id": ObjectId(id)})
    return helper_trainee(trainee_updated) if trainee_updated else None


# Eliminar datos del aprendiz
def delete_trainee(id: str):
    if not ObjectId.is_valid(id):
        return False
    result = collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0