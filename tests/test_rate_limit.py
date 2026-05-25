"""
Pruebas del middleware de limitación de tasa (rate limit) - FUN 12.
"""
import pytest
import time
from config import settings
from middlewares.rate_limit_middleware import peticiones


def test_rate_limit_middleware_exceeded(client):
    """fun_12: Verifica que el middleware bloquea las peticiones que superan el límite."""
    # Guardar valores originales
    original_limit = settings.RATE_LIMIT_LIMIT
    original_window = settings.RATE_LIMIT_WINDOW
    
    # Limpiar historial de peticiones
    peticiones.clear()
    
    try:
        # Configurar límites bajos para facilitar la prueba
        settings.RATE_LIMIT_LIMIT = 2
        settings.RATE_LIMIT_WINDOW = 5
        
        # Realizar 2 peticiones (deben ser permitidas, retornando 200 en la raíz)
        response1 = client.get("/")
        assert response1.status_code == 200
        
        response2 = client.get("/")
        assert response2.status_code == 200
        
        # La 3ra petición debe ser denegada con 429 Too Many Requests
        response3 = client.get("/")
        assert response3.status_code == 429
        assert response3.json() == {"detail": "Too Many Requests. Rate limit exceeded."}
        
    finally:
        # Restaurar valores originales
        settings.RATE_LIMIT_LIMIT = original_limit
        settings.RATE_LIMIT_WINDOW = original_window
        peticiones.clear()


def test_rate_limit_middleware_expires(client):
    """fun_12: Verifica que el límite se reinicie después de que expire la ventana de tiempo."""
    # Guardar valores originales
    original_limit = settings.RATE_LIMIT_LIMIT
    original_window = settings.RATE_LIMIT_WINDOW
    
    # Limpiar historial de peticiones
    peticiones.clear()
    
    try:
        # Configurar límites ultra-bajos para pruebas rápidas
        settings.RATE_LIMIT_LIMIT = 1
        settings.RATE_LIMIT_WINDOW = 1  # 1 segundo de ventana
        
        # Primera petición permitida
        response1 = client.get("/")
        assert response1.status_code == 200
        
        # Petición inmediata denegada
        response2 = client.get("/")
        assert response2.status_code == 429
        
        # Esperar a que pase la ventana de 1 segundo
        time.sleep(1.1)
        
        # Petición permitida tras expirar la ventana
        response3 = client.get("/")
        assert response3.status_code == 200
        
    finally:
        # Restaurar valores originales
        settings.RATE_LIMIT_LIMIT = original_limit
        settings.RATE_LIMIT_WINDOW = original_window
        peticiones.clear()
