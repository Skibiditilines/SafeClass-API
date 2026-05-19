"""
Pruebas del servicio de clima (OpenWeatherMap).
fun_07 — GET /weather          (clima actual del municipio)
fun_08 — GET /weather/{fecha}  (pronóstico por fecha, máx 5 días)
"""
import pytest
from datetime import date, timedelta
from unittest.mock import patch
from main import app
from middlewares.jwt_middleware import jwt_required


# ---------------------------------------------------------------------------
# Fixture: simula usuario autenticado (mismo patrón que test_suspensions.py)
# ---------------------------------------------------------------------------

def override_jwt_required():
    return {"sub": "1"}


@pytest.fixture
def auth_client(client):
    app.dependency_overrides[jwt_required] = override_jwt_required
    yield client
    app.dependency_overrides.pop(jwt_required, None)


# Municipio de prueba que devuelve el mock de la DB
MOCK_MUNICIPIO = {
    "id_municipio": 1,
    "nombre": "Hermosillo",
    "latitud": 29.0729,
    "longitud": -110.9559,
}

# Respuesta simulada de OWM para clima actual
MOCK_OWM_CURRENT = {
    "main": {"temp": 35.0, "feels_like": 38.0, "humidity": 20},
    "weather": [{"description": "cielo despejado"}],
    "wind": {"speed": 3.0},
    "rain": {},
}

# Un bloque horario de pronóstico tal como lo devuelve OWM /forecast
_HOY = str(date.today())
MOCK_OWM_FORECAST_BLOQUE = {
    "dt_txt": f"{_HOY} 12:00:00",
    "main": {"temp": 32.0, "feels_like": 35.0, "humidity": 25},
    "weather": [{"description": "nubes dispersas"}],
    "wind": {"speed": 2.5},
    "rain": {},
}


# ---------------------------------------------------------------------------
# fun_07 — GET /weather
# ---------------------------------------------------------------------------

def test_fun_07_clima_actual(auth_client, mock_db):
    """fun_07: Clima actual del municipio retorna 200 con campos esperados."""
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchone.return_value = MOCK_MUNICIPIO

    with patch(
        "services.openweathermap_service.get_current_weather",
        return_value=MOCK_OWM_CURRENT,
    ):
        response = auth_client.get("/weather/")

    assert response.status_code == 200
    data = response.json()
    assert data["municipio"] == "Hermosillo"
    assert "temperatura" in data
    assert "humedad" in data


def test_fun_07_sin_municipio(auth_client, mock_db):
    """fun_07: Si el usuario no tiene municipio vinculado retorna 404."""
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchone.return_value = None

    response = auth_client.get("/weather/")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# fun_08 — GET /weather/{fecha}
# ---------------------------------------------------------------------------

def test_fun_08_pronostico_por_fecha(auth_client, mock_db):
    """fun_08: Pronóstico para una fecha válida retorna 200 con lista de bloques."""
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchone.return_value = MOCK_MUNICIPIO

    fecha_valida = str(date.today() + timedelta(days=1))  # mañana

    with patch(
        "services.openweathermap_service.get_forecast",
        return_value={"lista": [MOCK_OWM_FORECAST_BLOQUE]},
    ):
        response = auth_client.get(f"/weather/{fecha_valida}")

    assert response.status_code == 200
    data = response.json()
    assert data["municipio"] == "Hermosillo"
    assert data["fecha"] == fecha_valida
    assert isinstance(data["pronostico"], list)
    assert len(data["pronostico"]) == 1
    assert "hora" in data["pronostico"][0]
    assert "temperatura" in data["pronostico"][0]


def test_fun_08_fecha_fuera_de_ventana(auth_client, mock_db):
    """fun_08: Fecha fuera de los 5 días permitidos retorna 400."""
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchone.return_value = MOCK_MUNICIPIO

    fecha_lejana = str(date.today() + timedelta(days=10))

    response = auth_client.get(f"/weather/{fecha_lejana}")
    assert response.status_code == 400


def test_fun_08_formato_fecha_invalido(auth_client, mock_db):
    """fun_08: Fecha con formato incorrecto retorna 422."""
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchone.return_value = MOCK_MUNICIPIO

    response = auth_client.get("/weather/18-05-2026")  # formato incorrecto
    assert response.status_code == 422


def test_fun_08_sin_municipio(auth_client, mock_db):
    """fun_08: Si el usuario no tiene municipio vinculado retorna 404."""
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchone.return_value = None

    fecha_valida = str(date.today() + timedelta(days=1))
    response = auth_client.get(f"/weather/{fecha_valida}")
    assert response.status_code == 404