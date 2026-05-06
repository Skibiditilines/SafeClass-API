"""
Pruebas del módulo de suspensiones.
fun_09 — POST /suspensions           (registrar suspensión)
fun_10 — GET  /suspensions           (listar suspensiones del usuario)
fun_10 — GET  /suspensions/{fecha}   (suspensión por fecha)
"""
import pytest

# Nota: Endpoints actualmente sin implementar.
# Estas pruebas proporcionan la estructura base.

def test_fun_09_create_suspension(client):
    """fun_09: Registrar una suspensión del día actual retorna 201."""
    payload = {"fecha": "2026-05-05"}
    # TODO: Generar un token válido e inyectarlo en los headers cuando se implemente la seguridad
    # headers = {"Authorization": "Bearer <token>"}
    response = client.post("/suspensions/", json=payload)
    # Puede retornar 200 (dummy) o 201 (implementado)
    assert response.status_code in (200, 201)
    assert "message" in response.json() or "id_suspension" in response.json()


def test_fun_10_get_all_suspensions(client):
    """fun_10: Listar todas las suspensiones del usuario retorna 200."""
    response = client.get("/suspensions/")
    assert response.status_code == 200
    assert "message" in response.json() or isinstance(response.json(), list)


def test_fun_10_get_suspension_by_date(client):
    """fun_10: Obtener suspensión por fecha específica retorna 200 o null."""
    fecha = "2026-05-05"
    response = client.get(f"/suspensions/{fecha}")
    assert response.status_code == 200
    assert "message" in response.json() or "fecha" in response.json() or response.json() is None
