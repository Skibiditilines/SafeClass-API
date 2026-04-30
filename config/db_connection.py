"""
Módulo para la conexión a la base de datos MySQL.
"""
import mysql.connector
from mysql.connector import Error
from config.settings import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

def get_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            yield connection
            
    except Error as e:
        print(f"Error al conectar a la base de datos MySQL: {e}")
        raise e
        
    finally:
        if connection is not None and connection.is_connected():
            connection.close()