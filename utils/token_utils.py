"""
Utilidades auxiliares relacionadas con tokens JWT.
Extracción del usuario actual desde el token, etc.
"""
import jwt
from fastapi import HTTPException, status
from config.settings import SECRET_KEY, ALGORITHM

def verify_token(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise ValueError("Token sin identificación de usuario")
            
        return int(user_id)
        
    except (jwt.PyJWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

