"""
Configuración general de la aplicación.
Lee variables de entorno para datos sensibles.
"""
import os
import dotenv

dotenv.load_dotenv()

# Base de datos
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# OpenWeatherMap
OWM_API_KEY = os.getenv("OWM_API_KEY")
OWM_BASE_URL = os.getenv("OWM_BASE_URL")

# Rate Limiting
RATE_LIMIT_LIMIT = int(os.getenv("RATE_LIMIT_LIMIT", "100"))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))

