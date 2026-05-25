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
    url = f"{OWM_BASE_URL}/forecast"

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
        data = response.json()
        
        # Filtrar bloques de pronóstico que correspondan a la fecha indicada
        blocks = data.get("list", [])
        filtered_blocks = [
            b for b in blocks if b.get("dt_txt", "").startswith(fecha)
        ]
        
        return {
            "city": data.get("city", {}),
            "list": filtered_blocks
        }

    except requests.exceptions.RequestException as e:
        print(f"Error al consultar el pronóstico: {e}")
        return {"error": str(e)}



