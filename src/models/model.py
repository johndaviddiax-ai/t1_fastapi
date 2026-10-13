from typing import Opcional
from pydantic import BaseModel, EmailStr

class TraineeModel(BaseModel):
    document: str
    firstname: str
    lastname: str
    email: EmailStr
    age: int
    program : str
    record_number: int
    
class TraineeUpdateModel(BaseModel):
    firstname: Opcional[str] = None
    lastname: Opcional[str] = None
    email: Opcional[EmailStr] = None
    age: Opcional[int] = None
    program : Opcional[str] = None
    record_number: Opcional[int] = None
    