import os 
from dotenv import load_dotenv
from src.etl.extract_transf import scrapeo_sephora
from src.etl.load import cargar_datos_sephora

load_dotenv()
ARCHIVO_SALIDA = os.getenv("ARCHIVO_SALIDA")
URL = os.getenv("URL")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def extraccion_transf_carga(archivo_salida, url, nombre_db, usuario, contraseña, servidor, puerto):
    try:
        try:
            df = scrapeo_sephora(url, archivo_salida)
        except Exception as e:
            raise Exception(f"Error en la extracción y transformación de datos: {e}")

        try:
            cargar_datos_sephora(df, nombre_db, usuario, contraseña, servidor, puerto)
        except Exception as e:
            raise Exception(f"Error en la creación de tablas y carga de datos en la base de datos: {e}")

    except Exception as e:
        raise Exception(f"Error en el proceso completo de extracción, transformación y carga: {e}")

extraccion_transf_carga(ARCHIVO_SALIDA, URL, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)