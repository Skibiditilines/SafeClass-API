"""
Rutas de suspensiones.
POST /suspensions           - Registrar una suspensión
GET  /suspensions           - Obtener todas las suspensiones del usuario
GET  /suspensions/{fecha}   - Obtener la suspensión de una fecha específica
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
    db = Depends(get_db_connection), 
    id_academico: int = Depends(jwt_required)
):
    """Registrar una suspensión en una fecha determinada."""
    return suspension_controller.create_suspension(db, id_academico, suspension.fecha)


@router.get("/")
def get_all_suspensions():
    """Obtener todas las suspensiones del usuario autenticado."""
    # TODO: Obtener id del académico del token JWT
    # TODO: Llamar a suspension_controller.get_all_suspensions(...)
    return {"message": "get all suspensions - not implemented yet"}


@router.get("/{fecha}")
def get_suspension_by_date(fecha: str):
    """Obtener la suspensión de una fecha específica (YYYY-MM-DD)."""
    # TODO: Llamar a suspension_controller.get_suspension_by_date(...)
    return {"message": f"get suspension for {fecha} - not implemented yet"}
