"""
Middleware de limitación de tasa (rate limiting).
Evita abuso de la API limitando el número de peticiones por cliente.
"""
# TODO: Implementar rate limiting (ej. con slowapi o una solución propia)


async def rate_limit_middleware(request, call_next):
    """
    Middleware que limita la cantidad de peticiones por IP/cliente.
    """
    response = await call_next(request)
    return response
