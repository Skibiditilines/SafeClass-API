"""
Controlador de municipios.
Maneja la obtención de municipios registrados.
"""
from fastapi import HTTPException, status
import mysql.connector
from models.municipality import MunicipioResponse


def get_all_municipalities(db) -> list[MunicipioResponse]:
    """Retorna todos los municipios registrados."""
    cursor = db.cursor(dictionary=True)
    try:
        # Seleccionar todos los municipios con sus coordenadas
        cursor.execute("SELECT id_municipio, nombre, lat, lon FROM MUNICIPIO")
        rows = cursor.fetchall()
        return [MunicipioResponse(**row) for row in rows]
    except mysql.connector.Error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error interno en el servidor de base de datos."
        )
    finally:
        cursor.close()


def get_municipality_by_id(db, municipio_id: int) -> MunicipioResponse:
    """Retorna un municipio específico por su ID."""
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id_municipio, nombre, lat, lon FROM MUNICIPIO WHERE id_municipio = %s",
            (municipio_id,)
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Municipio con id {municipio_id} no encontrado."
            )
        return MunicipioResponse(**row)
    except mysql.connector.Error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error interno en el servidor de base de datos."
        )
    finally:
        cursor.close()
