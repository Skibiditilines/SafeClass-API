"""
Pruebas del módulo de suspensiones.
fun_09 — POST /suspensions           (registrar suspensión)
fun_10 — GET  /suspensions           (listar suspensiones del usuario)
fun_10 — GET  /suspensions/{fecha}   (suspensión por fecha)
"""
import pytest
from main import app
from middlewares.jwt_middleware import jwt_required

def override_jwt_required():
    return 1  # Simula el id_academico = 1

@pytest.fixture
def auth_client(client):
    app.dependency_overrides[jwt_required] = override_jwt_required
    yield client
    app.dependency_overrides.pop(jwt_required, None)

def test_fun_09_create_suspension(auth_client, mock_db):
    """fun_09: Registrar una suspensión retorna 201 y los datos insertados."""
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchone.return_value = None  # No existe suspensión previa
    mock_cursor.lastrowid = 1
    
    payload = {"fecha": "2026-05-05"}
    response = auth_client.post("/suspensions/", json=payload)
    
    assert response.status_code == 201
    assert response.json()["id_suspension"] == 1
    assert response.json()["id_academico"] == 1
    assert response.json()["fecha"] == "2026-05-05"


def test_fun_10_get_all_suspensions(auth_client, mock_db):
    """fun_10: Listar todas las suspensiones del usuario retorna 200."""
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchall.return_value = [{"id_suspension": 1, "id_academico": 1, "fecha": "2026-05-05"}]
    
    response = auth_client.get("/suspensions/")
    assert response.status_code == 200
    assert "message" in response.json() or isinstance(response.json(), list)


def test_fun_10_get_suspension_by_date(auth_client, mock_db):
    """fun_10: Obtener suspensión por fecha específica retorna 200 o null."""
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchone.return_value = {"id_suspension": 1, "id_academico": 1, "fecha": "2026-05-05"}
    
    fecha = "2026-05-05"
    response = auth_client.get(f"/suspensions/{fecha}")
    assert response.status_code == 200
    assert "message" in response.json() or "fecha" in response.json() or response.json() is None
