from pydantic import BaseModel, EmailStr

class AcademicoBase(BaseModel):
    nombre: str
    institucion: str
    correo: EmailStr
    id_municipio: int

class AcademicoCreate(AcademicoBase):
    contrasena: str

class AcademicoResponse(AcademicoBase):
    id_academico: int

    class Config:
        from_attributes = True
