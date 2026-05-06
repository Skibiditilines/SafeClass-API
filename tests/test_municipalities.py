"""
Pruebas del módulo de municipios.
fun_05 — POST /municipios      (listar todos)
fun_06 — GET  /municipios/{id} (obtener por ID)
"""
import pytest

# Nota: Estos endpoints están actualmente sin implementar en el controlador.
# Las pruebas validan el comportamiento de los endpoints "dummy".
# Cuando se implemente la lógica real, estas pruebas deberán ser actualizadas
# para hacer mock de la base de datos (como en test_auth.py).

def test_fun_05_get_all_municipalities(client, mock_db):
    """fun_05: Listar todos los municipios retorna 200 y una lista."""
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchall.return_value = [
        {"id_municipio": 1, "nombre": "Test", "lat": 0.0, "lon": 0.0}
    ]
    response = client.get("/municipios/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_fun_06_get_municipality_by_id(client, mock_db):
    """fun_06: Obtener municipio por ID válido retorna sus datos."""
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchone.return_value = {
        "id_municipio": 1,
        "nombre": "Test",
        "lat": 0.0,
        "lon": 0.0
    }
    municipality_id = 1
    response = client.get(f"/municipios/{municipality_id}")
    assert response.status_code == 200
    assert "id_municipio" in response.json()
