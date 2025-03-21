import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Credenciales para el sitio web
CREDENTIALS = {
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD")
}

# Configuración de la base de datos MySQL
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

# URLs para scraping
URLS = {
    "base_url": "https://www.saucedemo.com/",
    "inventory": "https://www.saucedemo.com/inventory.html"
}
