"""
Pruebas del módulo de autenticación.
fun_01 — POST /auth/signup (registro exitoso)
fun_02 — POST /auth/signup (correo duplicado)
fun_03 — POST /auth/login  (login exitoso)
fun_04 — POST /auth/login  (credenciales incorrectas)
"""
import pytest
from unittest.mock import MagicMock
from utils.password_utils import hash_password

def test_fun_01_signup_success(client, mock_db):
    """fun_01: Registro exitoso de un académico."""
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchone.return_value = None  # No duplicate email
    mock_cursor.lastrowid = 1

    payload = {
        "nombre": "Juan Perez",
        "institucion": "UNAM",
        "correo": "juan.perez@example.com",
        "contrasena": "password123",
        "id_municipio": 1
    }

    response = client.post("/auth/signup", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["id_academico"] == 1
    assert data["correo"] == "juan.perez@example.com"
    assert "contrasena" not in data


def test_fun_02_signup_duplicate_email(client, mock_db):
    """fun_02: Registro con correo ya existente debe retornar error."""
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchone.return_value = {"id_academico": 1}  # Simulates duplicate email

    payload = {
        "nombre": "Juan Perez",
        "institucion": "UNAM",
        "correo": "duplicado@example.com",
        "contrasena": "password123",
        "id_municipio": 1
    }

    response = client.post("/auth/signup", json=payload)
    
    assert response.status_code == 400
    assert "registrado" in response.json()["detail"].lower()


def test_fun_03_login_success(client, mock_db):
    """fun_03: Login exitoso retorna token JWT."""
    mock_cursor = mock_db.cursor.return_value
    hashed_pw = hash_password("password123")
    mock_cursor.fetchone.return_value = {
        "id_academico": 1,
        "correo": "juan.perez@example.com",
        "contrasena": hashed_pw
    }

    payload = {
        "correo": "juan.perez@example.com",
        "contrasena": "password123"
    }

    response = client.post("/auth/login", json=payload)
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_fun_04_login_invalid_credentials(client, mock_db):
    """fun_04: Login con contraseña incorrecta retorna 401."""
    mock_cursor = mock_db.cursor.return_value
    hashed_pw = hash_password("password123")
    mock_cursor.fetchone.return_value = {
        "id_academico": 1,
        "correo": "juan.perez@example.com",
        "contrasena": hashed_pw
    }

    payload = {
        "correo": "juan.perez@example.com",
        "contrasena": "wrongpassword"
    }

    response = client.post("/auth/login", json=payload)
    
    assert response.status_code == 401
    assert "incorrecto" in response.json()["detail"].lower()
