"""
Definición del modelo de la tabla MUNICIPIO.
"""
from pydantic import BaseModel

class MunicipioBase(BaseModel):
    nombre: str
    lat: str
    lon: str

# Para respuestas de la API
class MunicipioResponse(MunicipioBase):
    id_municipio: int

    class Config:
        from_attributes = True
