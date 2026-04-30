"""
Controlador de autenticación.
Maneja el registro y login de académicos.
"""
from fastapi import HTTPException, status
import mysql.connector
from models.database import AcademicoCreate, AcademicoResponse
from utils.password_utils import hash_password

def signup(db, academico: AcademicoCreate) -> AcademicoResponse:
    cursor = db.cursor(dictionary=True)
    
    try:
        # Validación de correo duplicado
        cursor.execute("SELECT id_academico FROM ACADEMICO WHERE correo = %s", (academico.correo,))
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya se encuentra registrado."
            )

        # Generación de hash de seguridad para la contraseña
        hashed_pw = hash_password(academico.contrasena)

        # Inserción de datos
        query = """
            INSERT INTO ACADEMICO (nombre, institucion, correo, contrasena, id_municipio)
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (academico.nombre, academico.institucion, academico.correo, hashed_pw, academico.id_municipio)
        
        cursor.execute(query, valores)
        db.commit()
        
        # Retorno de la información del usuario
        return AcademicoResponse(
            id_academico=cursor.lastrowid,
            nombre=academico.nombre,
            institucion=academico.institucion,
            correo=academico.correo,
            id_municipio=academico.id_municipio
        )

    except mysql.connector.Error as err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la base de datos: {err}"
        )
    finally:
        cursor.close()


def login(correo: str, contrasena: str):
    """Autentica un académico y retorna un token JWT."""
    pass
