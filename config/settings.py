"""
Configuración general de la aplicación.
Lee variables de entorno para datos sensibles.
"""
import os

# Base de datos
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "safeclass_db")

# JWT
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# OpenWeatherMap
OWM_API_KEY = os.getenv("OWM_API_KEY", "")
OWM_BASE_URL = "https://api.openweathermap.org/data/2.5"
