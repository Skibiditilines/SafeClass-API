"""
Controlador de suspensiones.
Maneja el registro y consulta de suspensiones de actividades.
"""
import mysql.connector
from fastapi import HTTPException, status
from models.suspension import SuspensionResponse


def get_all_suspensions(db, academico_id: int) -> list[SuspensionResponse]:
    """Retorna todas las suspensiones registradas por el académico autenticado."""
    cursor = db.cursor(dictionary=True)
    try:
        # Traer todas las suspensiones que pertenecen al académico
        cursor.execute(
            "SELECT id_suspension, fecha, id_academico FROM SUSPENSION WHERE id_academico = %s",
            (academico_id,)
        )
        rows = cursor.fetchall()
        # Convertir cada fila a un objeto de respuesta
        return [SuspensionResponse(**row) for row in rows]
    except mysql.connector.Error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error interno en el servidor de base de datos."
        )
    finally:
        cursor.close()


def get_suspension_by_date(db, academico_id: int, fecha: str) -> SuspensionResponse:
    """Retorna la suspensión de una fecha específica del académico autenticado."""
    cursor = db.cursor(dictionary=True)
    try:
        # Buscar la suspensión que coincida con el académico y la fecha dada
        cursor.execute(
            "SELECT id_suspension, fecha, id_academico FROM SUSPENSION WHERE id_academico = %s AND fecha = %s",
            (academico_id, fecha)
        )
        row = cursor.fetchone()

        # Si no existe registro para esa fecha, devolver 404
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró una suspensión para la fecha {fecha}."
            )
        return SuspensionResponse(**row)
    except mysql.connector.Error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error interno en el servidor de base de datos."
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
