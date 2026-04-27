"""
Rutas de suspensiones.
POST /suspensions           - Registrar una suspensión
GET  /suspensions           - Obtener todas las suspensiones del usuario
GET  /suspensions/{fecha}   - Obtener la suspensión de una fecha específica
"""
from fastapi import APIRouter

router = APIRouter()


@router.post("/")
def create_suspension():
    """Registrar una suspensión en una fecha determinada."""
    # TODO: Recibir body con fecha
    # TODO: Llamar a suspension_controller.create_suspension(...)
    return {"message": "create suspension - not implemented yet"}


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
