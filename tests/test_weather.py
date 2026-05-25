"""
Pruebas del servicio de clima (OpenWeatherMap) - FUN 07 y FUN 08.
"""
import pytest
from unittest.mock import patch
from datetime import date, timedelta
from main import app
from middlewares.jwt_middleware import jwt_required

# Generar fechas dinámicas para evitar fallos por desfase temporal
TODAY = date.today()
TOMORROW = (TODAY + timedelta(days=1)).strftime("%Y-%m-%d")
FUTURE_DATE_OUT = (TODAY + timedelta(days=6)).strftime("%Y-%m-%d")


def override_jwt_required():
    return {"sub": "1"}  # Simula el payload JWT real (sub = id_academico como string)


@pytest.fixture
def auth_client(client):
    app.dependency_overrides[jwt_required] = override_jwt_required
    yield client
    app.dependency_overrides.pop(jwt_required, None)


def test_fun_07_clima_actual(auth_client, mock_db):
    """fun_07: Verifica que GET /weather/ retorne 200 y el JSON de clima formateado."""
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchone.return_value = {
        "id_municipio": 1,
        "nombre": "Xalapa",
        "latitud": 19.54,
        "longitud": -96.91
    }

    mock_weather_response = {
        "main": {"temp": 22.5, "feels_like": 21.0, "humidity": 70},
        "weather": [{"description": "cielo claro"}],
        "wind": {"speed": 3.0},
        "rain": {"1h": 0.5}
    }

    with patch("services.openweathermap_service.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_weather_response

        response = auth_client.get("/weather/")
        assert response.status_code == 200
        data = response.json()
        assert data["municipio"] == "Xalapa"
        assert data["temperatura"] == 22.5
        assert data["sensacion_termica"] == 21.0
        assert data["humedad"] == 70
        assert data["descripcion"] == "cielo claro"
        assert data["viento_kmh"] == round(3.0 * 3.6, 2)
        assert data["lluvia_mm"] == 0.5


def test_fun_07_sin_municipio(auth_client, mock_db):
    """fun_07: Verifica que GET /weather/ retorne 404 si el usuario no tiene municipio en BD."""
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchone.return_value = None  # Sin municipio vinculado

    response = auth_client.get("/weather/")
    assert response.status_code == 404
    assert "municipio" in response.json()["detail"].lower()


def test_fun_08_pronostico_por_fecha(auth_client, mock_db):
    """fun_08: Verifica que GET /weather/{fecha} retorne 200 para una fecha válida (mañana)."""
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchone.return_value = {
        "id_municipio": 1,
        "nombre": "Xalapa",
        "latitud": 19.54,
        "longitud": -96.91
    }

    mock_forecast_response = {
        "city": {"name": "Xalapa"},
        "list": [
            {
                "dt_txt": f"{TOMORROW} 12:00:00",
                "main": {"temp": 24.0, "feels_like": 23.0, "humidity": 65},
                "weather": [{"description": "nubes dispersas"}],
                "wind": {"speed": 4.0},
                "rain": {"3h": 1.0}
            }
        ]
    }

    with patch("services.openweathermap_service.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_forecast_response

        response = auth_client.get(f"/weather/{TOMORROW}")
        assert response.status_code == 200
        data = response.json()
        assert data["municipio"] == "Xalapa"
        assert data["fecha"] == TOMORROW
        assert len(data["pronostico"]) == 1
        assert data["pronostico"][0]["hora"] == "12:00:00"
        assert data["pronostico"][0]["temperatura"] == 24.0
        assert data["pronostico"][0]["viento_kmh"] == round(4.0 * 3.6, 2)
        assert data["pronostico"][0]["lluvia_mm"] == 1.0


def test_fun_08_fecha_fuera_de_ventana(auth_client):
    """fun_08: Verifica que retorne 400 si se pide una fecha mayor a 5 días en el futuro."""
    response = auth_client.get(f"/weather/{FUTURE_DATE_OUT}")
    assert response.status_code == 400
    assert "ventana" in response.json()["detail"].lower()


def test_fun_08_formato_fecha_invalido(auth_client):
    """fun_08: Verifica que retorne 400/422 si la fecha no tiene formato YYYY-MM-DD."""
    response_bad_format = auth_client.get("/weather/2026-05-32")
    assert response_bad_format.status_code in [400, 422]

    response_text = auth_client.get("/weather/fecha-invalida")
    assert response_text.status_code in [400, 422]


def test_fun_08_sin_municipio(auth_client, mock_db):
    """fun_08: Verifica que retorne 404 al consultar una fecha válida pero el usuario no tiene municipio."""
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchone.return_value = None  # Sin municipio vinculado

    response = auth_client.get(f"/weather/{TOMORROW}")
    assert response.status_code == 404
    assert "municipio" in response.json()["detail"].lower()
