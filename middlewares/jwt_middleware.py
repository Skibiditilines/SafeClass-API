"""
Middleware de autenticación JWT.
Protege las rutas que requieren un token válido.
"""
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.token_service import verify_token

security = HTTPBearer()

async def jwt_required(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    token = credentials.credentials
    return verify_token(token)