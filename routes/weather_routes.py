from fastapi import APIRouter, Depends, HTTPException, status
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