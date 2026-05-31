"""
Rutas de suspensiones.
POST /suspensions           - Registrar una suspensión
GET  /suspensions           - Obtener todas las suspensiones del usuario autenticado
GET  /suspensions/{fecha}   - Obtener la suspensión de una fecha específica (YYYY-MM-DD)
"""
from fastapi import APIRouter, Depends, status
from config.db_connection import get_db_connection
from middlewares.jwt_middleware import jwt_required
from models.suspension import SuspensionBase, SuspensionResponse
from controllers import suspension_controller

router = APIRouter()


@router.post("/", response_model=SuspensionResponse, status_code=status.HTTP_201_CREATED)
def create_suspension(
    suspension: SuspensionBase,
    db=Depends(get_db_connection),
    payload: dict = Depends(jwt_required)
):
    """Registrar una suspensión en una fecha determinada."""
    # El JWT almacena el id bajo la clave "sub" como string; se convierte a int
    id_academico = int(payload.get("sub"))
    return suspension_controller.create_suspension(db, id_academico, suspension.fecha)

# Fun_10: Ethan Sarricolea
@router.get(
    "/",
    response_model=list[SuspensionResponse],
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
def get_all_suspensions(
    db=Depends(get_db_connection),
    payload: dict = Depends(jwt_required)
):
    """Obtener todas las suspensiones del usuario autenticado."""
    # El JWT almacena el id bajo la clave "sub" como string; se convierte a int
    id_academico = int(payload.get("sub"))
    return suspension_controller.get_all_suspensions(db, id_academico)

@router.get("/recommendations", status_code=status.HTTP_200_OK)
def get_suspension_recommendations(
    db=Depends(get_db_connection),
    payload: dict = Depends(jwt_required)
):
    """Obtener recomendaciones de suspensión para los próximos días según el clima."""
    id_academico = int(payload.get("sub"))
    return suspension_controller.get_suspension_recommendations(db, id_academico)


@router.get(
    "/{fecha}",
    response_model=SuspensionResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "description": "Suspensión no encontrada",
            "content": {
                "application/json": {
                    "example": {"detail": "No se encontró una suspensión para la fecha 2026-05-07."}
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
def get_suspension_by_date(
    fecha: str,
    db=Depends(get_db_connection),
    payload: dict = Depends(jwt_required)
):
    """Obtener la suspensión de una fecha específica (YYYY-MM-DD)."""
    # El JWT almacena el id bajo la clave "sub" como string; se convierte a int
    id_academico = int(payload.get("sub"))
    return suspension_controller.get_suspension_by_date(db, id_academico, fecha)

