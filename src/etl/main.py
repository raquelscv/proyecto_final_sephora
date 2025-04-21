import os 
from dotenv import load_dotenv
from .extract_transf import scrapeo_sephora

load_dotenv()
ARCHIVO_SALIDA = os.getenv("ARCHIVO_SALIDA")
URL = os.getenv("URL")
