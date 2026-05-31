"""
Controlador de suspensiones.
Maneja el registro y consulta de suspensiones de actividades.
"""
import mysql.connector
from fastapi import HTTPException, status
from models.suspension import SuspensionResponse
from datetime import date, timedelta
from services import openweathermap_service
from services.suspension_recommendation_service import evaluar_riesgo
from fastapi import HTTPException
from services import openweathermap_service
from services.suspension_recommendation_service import evaluar_riesgo


def get_all_suspensions(db, academico_id: int) -> list[SuspensionResponse]:
    """Retorna todas las suspensiones registradas por el académico autenticado."""
    cursor = db.cursor(dictionary=True)
    try:
        # Traer todas las suspensiones que pertenecen al académico
        cursor.execute(
            "SELECT id_suspension, fecha, id_academico FROM SUSPENSION WHERE id_academico = %s",
            (academico_id,)
        )
        rows = cursor.fetchall()
        # Convertir cada fila a un objeto de respuesta
        return [SuspensionResponse(**row) for row in rows]
    except mysql.connector.Error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error interno en el servidor de base de datos."
        )
    finally:
        cursor.close()


def get_suspension_by_date(db, academico_id: int, fecha: str) -> SuspensionResponse:
    """Retorna la suspensión de una fecha específica del académico autenticado."""
    cursor = db.cursor(dictionary=True)
    try:
        # Buscar la suspensión que coincida con el académico y la fecha dada
        cursor.execute(
            "SELECT id_suspension, fecha, id_academico FROM SUSPENSION WHERE id_academico = %s AND fecha = %s",
            (academico_id, fecha)
        )
        row = cursor.fetchone()

        # Si no existe registro para esa fecha, devolver 404
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró una suspensión para la fecha {fecha}."
            )
        return SuspensionResponse(**row)
    except mysql.connector.Error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error interno en el servidor de base de datos."
        )
    finally:
        cursor.close()


def create_suspension(db, academico_id: int, fecha):
    """Registra una nueva suspensión para el académico."""
    cursor = db.cursor(dictionary=True)
    try:
        # Verificar si ya existe
        cursor.execute("SELECT id_suspension FROM SUSPENSION WHERE id_academico = %s AND fecha = %s", (academico_id, fecha))
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe una suspensión registrada para la fecha {fecha}."
            )
            
        cursor.execute("INSERT INTO SUSPENSION (fecha, id_academico) VALUES (%s, %s)", (fecha, academico_id))
        db.commit()
        return {
            "id_suspension": cursor.lastrowid,
            "id_academico": academico_id,
            "fecha": fecha
        }
    except mysql.connector.Error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al registrar la suspensión."
        )
    finally:
        cursor.close()

def get_suspension_recommendations(db, id_academico: int):
    municipio = obtener_municipio_del_academico(db, id_academico)

    if not municipio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no tiene municipio asignado."
        )

    lat = municipio["latitud"]
    lon = municipio["longitud"]

    recomendaciones = []

    for i in range(0, 6):
        fecha = (date.today() + timedelta(days=i)).strftime("%Y-%m-%d")

        data = openweathermap_service.get_forecast(lat, lon, fecha)

        if "error" in data:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Error al consultar OpenWeatherMap: {data['error']}"
            )

        bloques = data.get("list", [])

        if not bloques:
            continue

        bloque_principal = bloques[len(bloques) // 2]

        clima = {
            "temperatura": bloque_principal.get("main", {}).get("temp"),
            "sensacion_termica": bloque_principal.get("main", {}).get("feels_like"),
            "humedad": bloque_principal.get("main", {}).get("humidity"),
            "descripcion": bloque_principal.get("weather", [{}])[0].get("description"),
            "viento_kmh": round(bloque_principal.get("wind", {}).get("speed", 0) * 3.6, 2),
            "lluvia_mm": bloque_principal.get("rain", {}).get("3h", 0.0) if bloque_principal.get("rain") else 0.0,
        }

        evaluacion = evaluar_riesgo(clima)

        recomendaciones.append({
            "fecha": fecha,
            "riesgo": evaluacion["riesgo"],
            "recomendacion": evaluacion["recomendacion"],
            "motivos": evaluacion["motivos"],
            "clima": clima
        })

    return {
        "municipio": municipio["nombre"],
        "recomendaciones": recomendaciones
    }
    
def obtener_municipio_del_academico(db, id_academico: int):
    cursor = db.cursor(dictionary=True)
    try:
        query = """
            SELECT 
                m.id_municipio,
                m.nombre,
                m.lat AS latitud,
                m.lon AS longitud
            FROM ACADEMICO a
            JOIN MUNICIPIO m ON a.id_municipio = m.id_municipio
            WHERE a.id_academico = %s
        """
        cursor.execute(query, (id_academico,))
        return cursor.fetchone()
    except mysql.connector.Error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error interno en el servidor de base de datos."
        )
    finally:
        cursor.close()