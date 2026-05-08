"""
Controlador del clima.
Contiene la lógica de negocio para consultar el clima de un municipio.
"""

from fastapi import HTTPException, status
import services.openweathermap_service as owm_service


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