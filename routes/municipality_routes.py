"""
Rutas de municipios.
GET  /municipios/{id} - Obtener un municipio específico
POST /municipios      - Obtener todos los municipios registrados
"""
from fastapi import APIRouter

router = APIRouter()


@router.post("/")
def get_all_municipalities():
    """Obtener todos los municipios registrados."""
    # TODO: Llamar a municipality_controller.get_all_municipalities()
    return {"message": "get all municipalities - not implemented yet"}


@router.get("/{id}")
def get_municipality(id: int):
    """Obtener un municipio específico por ID."""
    # TODO: Llamar a municipality_controller.get_municipality_by_id(id)
    return {"message": f"get municipality {id} - not implemented yet"}
