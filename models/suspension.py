"""
Definición del modelo de la tabla SUSPENSION.
"""
from pydantic import BaseModel
from datetime import date

class SuspensionBase(BaseModel):
    fecha: date

# Para crear una nueva suspensión (POST /suspensions)
class SuspensionCreate(SuspensionBase):
    id_academico: int

# Para listar el historial (GET /suspensions)
class SuspensionResponse(SuspensionBase):
    id_suspension: int
    id_academico: int

    class Config:
        from_attributes = True