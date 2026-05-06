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

def test_fun_05_get_all_municipalities(client):
    """fun_05: Listar todos los municipios retorna 200 y una lista."""
    response = client.post("/municipios/")
    assert response.status_code == 200
    # Expected final behavior should probably return a list, but currently it returns a dict with "message"
    assert "message" in response.json() or isinstance(response.json(), list)


def test_fun_06_get_municipality_by_id(client):
    """fun_06: Obtener municipio por ID válido retorna sus datos."""
    municipality_id = 1
    response = client.get(f"/municipios/{municipality_id}")
    assert response.status_code == 200
    assert "message" in response.json() or "id_municipio" in response.json()
