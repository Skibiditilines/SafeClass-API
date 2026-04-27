"""
Rutas de autenticación.
POST /auth/signup  - Registro de académico
POST /auth/login   - Login y generación de token JWT
"""
from fastapi import APIRouter

router = APIRouter()


@router.post("/signup")
def signup():
    """Registrar un nuevo académico en el sistema."""
    # TODO: Recibir body con nombre, institucion, correo, contrasena, municipio
    # TODO: Llamar a auth_controller.signup(...)
    return {"message": "signup endpoint - not implemented yet"}


@router.post("/login")
def login():
    """Autenticar usuario y generar token de acceso."""
    # TODO: Recibir body con correo, contrasena
    # TODO: Llamar a auth_controller.login(...)
    return {"message": "login endpoint - not implemented yet"}
