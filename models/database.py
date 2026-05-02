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

class LoginRequest(BaseModel):
    correo: EmailStr
    contrasena: str

class Token(BaseModel):
    access_token: str
    token_type: str