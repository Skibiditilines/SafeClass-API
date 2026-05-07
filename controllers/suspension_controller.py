"""
Controlador de suspensiones.
Maneja el registro y consulta de suspensiones de actividades.
"""
import mysql.connector
from fastapi import HTTPException, status

# TODO: Implementar lógica de suspensiones para GET

def get_all_suspensions(academico_id: int):
    """Retorna todas las suspensiones del académico."""
    pass


def get_suspension_by_date(academico_id: int, fecha: str):
    """Retorna la suspensión de una fecha específica (YYYY-MM-DD)."""
    pass


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
