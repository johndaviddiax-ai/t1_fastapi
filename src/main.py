from src.templates.controllers import (
    create_trainee, get_all_trainees, get_trainee_by_id,
    update_trainee, delete_trainee, get_trainee_by_document
)
from src.models.model import TraineeModel, TraineeUpdateModel
from fastapi import FastAPI, HTTPException, status

app = FastAPI(
    title="Gestion de datos de los aprendices",
    description="Api simple con FastAPI para consumir los datos de los aprendices",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {"message": "Hello world"}


@app.post("/trainee/", response_description="Registrar a un nuevo aprendiz",
          status_code=status.HTTP_201_CREATED)
def create_trainee_api(trainee: TraineeModel):
    if get_trainee_by_document(trainee.document):
        raise HTTPException(status_code=400, detail="Ya existe un aprendiz con ese documento")
    return create_trainee(trainee)


@app.get("/trainee/", response_description="Listar todos los aprendices")
def get_all_trainee_api():
    return get_all_trainees()


@app.get("/trainee/{id}", response_description="Obtener un aprendiz por su id")
def get_trainee_by_id_api(id: str):
    trainee = get_trainee_by_id(id)
    if not trainee:
        raise HTTPException(status_code=404, detail="Aprendiz no encontrado")
    return trainee


@app.put("/trainee/{id}", response_description="Actualizar datos de un aprendiz por su id")
def update_trainee_api(id: str, trainee: TraineeUpdateModel):
    updated = update_trainee(id, trainee)
    if not updated:
        raise HTTPException(status_code=404, detail="Aprendiz no encontrado")
    return updated


@app.delete("/trainee/{id}", response_description="Eliminar datos de un aprendiz")
def delete_trainee_api(id: str):
    if not delete_trainee(id):
        raise HTTPException(status_code=404, detail="Aprendiz no encontrado")
    return {"mensaje": "Aprendiz eliminado correctamente"}