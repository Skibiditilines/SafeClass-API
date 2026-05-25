"""
Middleware de limitación de tasa (rate limiting).
Evita abuso de la API limitando el número de peticiones por cliente.
"""
import time
from fastapi import Request
from fastapi.responses import JSONResponse
from config import settings

# Historial de peticiones en memoria: client_ip -> list of timestamps
peticiones = {}


async def rate_limit_middleware(request: Request, call_next):
    """
    Middleware que limita la cantidad de peticiones por IP/cliente.
    """
    client_ip = request.client.host if request.client else "unknown"
    ahora = time.time()
    
    # Inicializar registro de la IP
    if client_ip not in peticiones:
        peticiones[client_ip] = []
        
    # Filtrar peticiones obsoletas fuera de la ventana de tiempo
    peticiones[client_ip] = [t for t in peticiones[client_ip] if ahora - t < settings.RATE_LIMIT_WINDOW]
    
    # Validar si supera el límite establecido
    if len(peticiones[client_ip]) >= settings.RATE_LIMIT_LIMIT:
        return JSONResponse(
            status_code=429,
            content={"detail": "Too Many Requests. Rate limit exceeded."}
        )

        
    # Registrar la petición actual
    peticiones[client_ip].append(ahora)
    
    response = await call_next(request)
    return response

