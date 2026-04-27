"""
Servicio de consulta a la API de OpenWeatherMap.
Obtiene datos climáticos actuales y pronósticos.
"""
# TODO: Implementar las llamadas a la API de OpenWeatherMap


def get_current_weather(lat: float, lon: float) -> dict:
    """
    Obtiene el clima actual para las coordenadas dadas.
    Endpoint OWM: /weather
    """
    pass


def get_forecast(lat: float, lon: float, fecha: str) -> dict:
    """
    Obtiene el pronóstico para una fecha específica (máx. 5 días).
    Endpoint OWM: /forecast
    """
    pass
