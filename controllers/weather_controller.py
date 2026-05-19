"""
Controlador del clima.
Contiene la lógica de negocio para consultar el clima de un municipio.
"""

from fastapi import HTTPException, status
import services.openweathermap_service as owm_service
from datetime import date, timedelta
import re

def get_current_weather(municipio: dict) -> dict:
    lat = municipio.get("latitud")
    lon = municipio.get("longitud")

    if lat is None or lon is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El municipio no tiene coordenadas registradas.",
        )

    data = owm_service.get_current_weather(lat, lon)

    if "error" in data:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error al consultar OpenWeatherMap: {data['error']}",
        )
    
    return {
        "municipio": municipio.get("nombre"),
        "temperatura": data.get("main", {}).get("temp"),
        "sensacion_termica": data.get("main", {}).get("feels_like"),
        "humedad": data.get("main", {}).get("humidity"),
        "descripcion": data.get("weather", [{}])[0].get("description"),
        "viento_kmh": round(data.get("wind", {}).get("speed", 0) * 3.6, 2),
        "lluvia_mm": data.get("rain", {}).get("1h", 0),
    }


def get_weather_forecast(municipio: dict, fecha: str) -> dict:
    """
    Devuelve el pronóstico de clima por franja horaria para una fecha dada.
    La API de OWM /forecast cubre máx. 5 días desde el momento de la consulta.
    """

    # Validar formato YYYY-MM-DD
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fecha):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El formato de fecha debe ser YYYY-MM-DD.",
        )

    # Validar que la fecha esté dentro de la ventana de 5 días
    hoy = date.today()
    limite = hoy + timedelta(days=5)
    try:
        fecha_dt = date.fromisoformat(fecha)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Fecha inválida.",
        )

    if fecha_dt < hoy or fecha_dt > limite:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La fecha debe estar entre hoy ({hoy}) y los próximos 5 días ({limite}).",
        )

    lat = municipio.get("latitud")
    lon = municipio.get("longitud")

    if lat is None or lon is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El municipio no tiene coordenadas registradas.",
        )

    data = owm_service.get_forecast(lat, lon, fecha)

    if "error" in data:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error al consultar OpenWeatherMap: {data['error']}",
        )

    # Formatear cada bloque horario devuelto por OWM
    pronostico = [
        {
            "hora": bloque.get("dt_txt", "").split(" ")[-1][:5],  # HH:MM
            "temperatura": bloque.get("main", {}).get("temp"),
            "sensacion_termica": bloque.get("main", {}).get("feels_like"),
            "humedad": bloque.get("main", {}).get("humidity"),
            "descripcion": bloque.get("weather", [{}])[0].get("description"),
            "viento_kmh": round(bloque.get("wind", {}).get("speed", 0) * 3.6, 2),
            "lluvia_mm": bloque.get("rain", {}).get("3h", 0),
        }
        for bloque in data.get("lista", [])
    ]

    return {
        "municipio": municipio.get("nombre"),
        "fecha": fecha,
        "pronostico": pronostico,
    }