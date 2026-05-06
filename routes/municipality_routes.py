"""
Rutas de municipios.
GET /municipios/    - Obtener todos los municipios registrados
GET /municipios/{id} - Obtener un municipio específico
"""
from fastapi import APIRouter, Depends, status
from config.db_connection import get_db_connection
from models.municipality import MunicipioResponse
from controllers import municipality_controller

router = APIRouter()


@router.get(
    "/",
    response_model=list[MunicipioResponse],
    status_code=status.HTTP_200_OK,
    responses={
        500: {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {"detail": "Ocurrió un error interno en el servidor de base de datos."}
                }
            }
        }
    }
)
def get_all_municipalities(db=Depends(get_db_connection)):
    """Obtener todos los municipios registrados."""
    return municipality_controller.get_all_municipalities(db)


@router.get(
    "/{id}",
    response_model=MunicipioResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "description": "Municipio no encontrado",
            "content": {
                "application/json": {
                    "example": {"detail": "Municipio con id 1 no encontrado."}
                }
            }
        },
        500: {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {"detail": "Ocurrió un error interno en el servidor de base de datos."}
                }
            }
        }
    }
)
def get_municipality(id: int, db=Depends(get_db_connection)):
    """Obtener un municipio específico por ID."""
    return municipality_controller.get_municipality_by_id(db, id)
