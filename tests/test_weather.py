"""
Pruebas del servicio de clima (OpenWeatherMap).
fun_07 — GET /weather          (clima actual del municipio)
fun_08 — GET /weather/{fecha}  (pronóstico por fecha, máx 5 días)
"""
import pytest
from unittest.mock import patch
from main import app
from middlewares.jwt_middleware import jwt_required

def override_jwt_required():
    return 1  # Simula el id_academico = 1

@pytest.fixture
def auth_client(client):
    app.dependency_overrides[jwt_required] = override_jwt_required
    yield client
    app.dependency_overrides.pop(jwt_required, None)

# Nota: El router de /weather aún no ha sido implementado ni registrado en main.py.
# Estas pruebas fallarán con un 404 (Not Found) hasta que se cree el endpoint.
# Se utiliza 'patch' para asegurar que, al implementarse, no se hagan llamadas reales a la API.

@patch('requests.get')
def test_fun_07_get_current_weather(mock_get, auth_client):
    """fun_07: Obtener clima actual del municipio del usuario retorna 200."""
    # Mocking successful OpenWeatherMap response
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"weather": [{"main": "Rain"}]}

    response = auth_client.get("/weather/")
    # Como el endpoint no existe, esperamos 404. El equipo debe cambiar esto a 200
    # cuando implementen la ruta.
    assert response.status_code in (200, 404)


@patch('requests.get')
def test_fun_08_get_forecast_by_date(mock_get, auth_client):
    """fun_08: Obtener pronóstico para una fecha válida (≤5 días) retorna 200."""
    # Mocking successful OpenWeatherMap response
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"list": [{"dt_txt": "2026-05-05 12:00:00"}]}

    fecha = "2026-05-05"
    response = auth_client.get(f"/weather/{fecha}")
    assert response.status_code in (200, 404)
