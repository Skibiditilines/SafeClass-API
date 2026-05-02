"""
Rutas de autenticación.
POST /auth/signup  - Registro de académico
POST /auth/login   - Login y generación de token JWT
"""
from fastapi import APIRouter, Depends, status
from config.db_connection import get_db_connection
from models.database import AcademicoCreate, AcademicoResponse, LoginRequest, Token
from controllers import auth_controller

router = APIRouter()

@router.post(
    "/signup", 
    response_model=AcademicoResponse, 
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {
            "description": "Error de validación (Ej. Correo duplicado, Municipio inválido o Exceso de caracteres)",
            "content": {
                "application/json": {
                    "example": {"detail": "El correo electrónico ya se encuentra registrado."}
                }
            }
        },
        500: {
            "description": "Error interno del servidor (Fallo en la conexión o en la base de datos)",
            "content": {
                "application/json": {
                    "example": {"detail": "Ocurrió un error interno en el servidor de base de datos."}
                }
            }
        }
    }
)
def signup(academico: AcademicoCreate, db=Depends(get_db_connection)):
    return auth_controller.signup(db, academico)

@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "description": "Error de validación (Ej. Credenciales incorrectas)",
            "content": {
                "application/json": {
                    "example": {"detail": "Correo o contraseña incorrectos."}
                }
            }
        }
    } 
)  
def login(login_request: LoginRequest, db=Depends(get_db_connection)):
    return auth_controller.login(db, login_request.correo, login_request.contrasena)