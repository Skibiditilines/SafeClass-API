"""
Servicio de consulta a la API de OpenWeatherMap.
Obtiene datos climáticos actuales y pronósticos.
"""

import requests
from config.settings import OWM_API_KEY, OWM_BASE_URL


def get_current_weather(lat: float, lon: float) -> dict:
    url = f"{OWM_BASE_URL}/weather"

    # Parámetros de consulta para obtener el clima actual
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OWM_API_KEY,
        "units": "metric",
        "lang": "es",
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error al consultar el clima: {e}")
        return {"error": str(e)}


def get_forecast(lat: float, lon: float, fecha: str) -> dict:
    """
    Obtiene el pronóstico para una fecha específica (máx. 5 días).
    Endpoint OWM: /forecast
    """
    pass
