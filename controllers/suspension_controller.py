"""
Controlador de suspensiones.
Maneja el registro y consulta de suspensiones de actividades.
"""
import mysql.connector
from fastapi import HTTPException, status

# TODO: Implementar lógica de suspensiones para GET

def get_all_suspensions(db, academico_id: int):
    """Retorna todas las suspensiones del académico."""
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM SUSPENSION WHERE id_academico = %s ORDER BY fecha DESC", (academico_id,))
        return cursor.fetchall()
    except mysql.connector.Error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar las suspensiones."
        )
    finally:
        cursor.close()


def get_suspension_by_date(db, academico_id: int, fecha):
    """Retorna la suspensión de una fecha específica (YYYY-MM-DD)."""
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM SUSPENSION WHERE id_academico = %s AND fecha = %s", (academico_id, fecha))
        suspension = cursor.fetchone()
        if not suspension:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró una suspensión para la fecha {fecha}."
            )
        return suspension
    except mysql.connector.Error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la suspensión."
        )
    finally:
        cursor.close()


def create_suspension(db, academico_id: int, fecha):
    """Registra una nueva suspensión para el académico."""
    cursor = db.cursor(dictionary=True)
    try:
        # Verificar si ya existe
        cursor.execute("SELECT id_suspension FROM SUSPENSION WHERE id_academico = %s AND fecha = %s", (academico_id, fecha))
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe una suspensión registrada para la fecha {fecha}."
            )
            
        cursor.execute("INSERT INTO SUSPENSION (fecha, id_academico) VALUES (%s, %s)", (fecha, academico_id))
        db.commit()
        return {
            "id_suspension": cursor.lastrowid,
            "id_academico": academico_id,
            "fecha": fecha
        }
    except mysql.connector.Error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al registrar la suspensión."
        )
    finally:
        cursor.close()
