from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, date, timedelta
from config.db_connection import get_db_connection
from middlewares.jwt_middleware import jwt_required
import controllers.weather_controller as weather_ctrl

router = APIRouter()


def get_user_municipality(db, user_id: int):
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT m.id_municipio, m.nombre, m.lat AS latitud, m.lon AS longitud 
        FROM ACADEMICO u
        JOIN MUNICIPIO m ON u.id_municipio = m.id_municipio
        WHERE u.id_academico = %s
    """
    cursor.execute(query, (user_id,))
    municipio = cursor.fetchone()
    cursor.close()
    return municipio


@router.get("/")
def get_user_weather(
    db=Depends(get_db_connection),
    payload: dict = Depends(jwt_required)
):
    """Obtiene el clima actual del municipio del usuario autenticado."""
    user_id = int(payload.get("sub"))
    municipio = get_user_municipality(db, user_id)

    if not municipio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no tiene un municipio vinculado o no existe."
        )
    
    return weather_ctrl.get_current_weather(municipio)


@router.get("/{fecha}")
def get_user_forecast(
    fecha: str,
    db=Depends(get_db_connection),
    payload: dict = Depends(jwt_required)
):
    """Obtiene el pronóstico del municipio del usuario autenticado para una fecha específica (máx 5 días)."""
    try:
        target_date = datetime.strptime(fecha, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de fecha inválido. Debe ser YYYY-MM-DD."
        )
    
    today = date.today()
    max_date = today + timedelta(days=5)
    
    if target_date < today or target_date > max_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha solicitada está fuera de la ventana de pronóstico (máximo 5 días)."
        )
         
    user_id = int(payload.get("sub"))
    municipio = get_user_municipality(db, user_id)

    if not municipio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no tiene un municipio vinculado o no existe."
        )
        
    return weather_ctrl.get_forecast_by_date(municipio, fecha)
