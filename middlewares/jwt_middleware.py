"""
Middleware de autenticación JWT.
Protege las rutas que requieren un token válido.
"""
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


async def jwt_required(credentials: HTTPAuthorizationCredentials = security):
    """
    Dependencia de FastAPI que valida el token JWT en el header Authorization.
    Lanza HTTPException 401 si el token no es válido o ha expirado.
    """
    # TODO: Implementar validación del token
    token = credentials.credentials
    pass
