"""
Pruebas del módulo de autenticación.
fun_01 — POST /auth/signup (registro exitoso)
fun_02 — POST /auth/signup (correo duplicado)
fun_03 — POST /auth/login  (login exitoso)
fun_04 — POST /auth/login  (credenciales incorrectas)
"""
# TODO: Configurar cliente de pruebas (TestClient de FastAPI / httpx)
# from fastapi.testclient import TestClient
# from main import app
# client = TestClient(app)


def test_fun_01_signup_success():
    """fun_01: Registro exitoso de un académico."""
    pass


def test_fun_02_signup_duplicate_email():
    """fun_02: Registro con correo ya existente debe retornar error."""
    pass


def test_fun_03_login_success():
    """fun_03: Login exitoso retorna token JWT."""
    pass


def test_fun_04_login_invalid_credentials():
    """fun_04: Login con contraseña incorrecta retorna 401."""
    pass
