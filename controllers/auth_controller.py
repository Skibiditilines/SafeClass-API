"""
Controlador de autenticación.
Maneja el registro y login de académicos.
"""
from fastapi import HTTPException, status
import mysql.connector
from models.database import AcademicoCreate, AcademicoResponse
from services.token_service import create_access_token
from utils.password_utils import hash_password, verify_password
from mysql.connector import errorcode

def signup(db, academico: AcademicoCreate) -> AcademicoResponse:
    cursor = db.cursor(dictionary=True)
    
    try:
        # Validación preventiva de correo duplicado
        cursor.execute("SELECT id_academico FROM ACADEMICO WHERE correo = %s", (academico.correo,))
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya se encuentra registrado."
            )

        hashed_pw = hash_password(academico.contrasena)

        query = """
            INSERT INTO ACADEMICO (nombre, institucion, correo, contrasena, id_municipio)
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (academico.nombre, academico.institucion, academico.correo, hashed_pw, academico.id_municipio)
        
        cursor.execute(query, valores)
        db.commit()
        
        return AcademicoResponse(
            id_academico=cursor.lastrowid,
            nombre=academico.nombre,
            institucion=academico.institucion,
            correo=academico.correo,
            id_municipio=academico.id_municipio
        )

    except mysql.connector.Error as err:
        db.rollback()

        if err.errno == errorcode.ER_NO_REFERENCED_ROW_2: 
            # Violación de llave foránea
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El municipio especificado no existe o es inválido."
            )
        elif err.errno == errorcode.ER_DUP_ENTRY: 
            # Entrada duplicada
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un dato único (como el correo) ya se encuentra registrado."
            )
        elif err.errno == errorcode.ER_DATA_TOO_LONG: 
            # Dato excede el tamaño de la columna
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uno de los campos excede la longitud máxima permitida."
            )
        else:
            # Error de servidor para caídas de conexión o errores sintácticos
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ocurrió un error interno en el servidor de base de datos."
            )
            
    finally:
        cursor.close()


def login(db, correo: str, contrasena: str):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM ACADEMICO WHERE correo = %s", (correo,))
        academico = cursor.fetchone()
        
        if not academico or not verify_password(contrasena, academico['contrasena']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Correo o contraseña incorrectos."
            )

        token_data = {"sub": str(academico['id_academico'])}
        access_token = create_access_token(token_data)

        return {"access_token": access_token, "token_type": "bearer"}
    except mysql.connector.Error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error interno en el servidor de base de datos."
        )
    finally:
        cursor.close()