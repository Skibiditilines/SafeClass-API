"""
Rutas de autenticación.
POST /auth/signup  - Registro de académico
POST /auth/login   - Login y generación de token JWT
"""
from fastapi import APIRouter, Depends
from config.db_connection import get_db_connection
from models.database import AcademicoCreate, AcademicoResponse
from controllers import auth_controller

router = APIRouter()


@router.post("/signup", response_model=AcademicoResponse, status_code=201)
def signup(academico: AcademicoCreate, db=Depends(get_db_connection)):
    return auth_controller.signup(db, academico)

@router.post("/login")
def login():
    """Autenticar usuario y generar token de acceso."""
    # TODO: Recibir body con correo, contrasena
    # TODO: Llamar a auth_controller.login(...)
    return {"message": "login endpoint - not implemented yet"}

