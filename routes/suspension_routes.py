"""
Rutas de suspensiones.
POST /suspensions           - Registrar una suspensión
GET  /suspensions           - Obtener todas las suspensiones del usuario
GET  /suspensions/{fecha}   - Obtener la suspensión de una fecha específica
"""
from fastapi import APIRouter, Depends, status
from typing import List
from datetime import date
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


@router.get("/", response_model=List[SuspensionResponse])
def get_all_suspensions(
    db = Depends(get_db_connection), 
    id_academico: int = Depends(jwt_required)
):
    """Obtener todas las suspensiones del usuario autenticado."""
    return suspension_controller.get_all_suspensions(db, id_academico)


@router.get("/{fecha}", response_model=SuspensionResponse)
def get_suspension_by_date(
    fecha: date, 
    db = Depends(get_db_connection), 
    id_academico: int = Depends(jwt_required)
):
    """Obtener la suspensión de una fecha específica (YYYY-MM-DD)."""
    return suspension_controller.get_suspension_by_date(db, id_academico, fecha)
