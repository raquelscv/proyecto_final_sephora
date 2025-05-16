import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

def conectar_bd():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    return conn, conn.cursor()

def ejecutar_query(query):
    conn, cur = conectar_bd()
    cur.execute(query)
    cols = [desc[0] for desc in cur.description]
    datos = cur.fetchall()
    cur.close()
    conn.close()
    return pd.DataFrame(datos, columns=cols)

def info_reporte(dataframe):
    """
    Genera un informe sobre los valores nulos y tipos de datos de un DataFrame.

    Args:
        dataframe (pd.DataFrame): El DataFrame a analizar.

    Returns:
        pd.DataFrame: Un DataFrame con el número y porcentaje de valores nulos por columna,
                      junto con el tipo de dato de cada columna.
    """
    df_report = pd.DataFrame()
    df_report["Numero_nulos"] = dataframe.isnull().sum()
    df_report["Porcentaje_nulos"] = round((dataframe.isnull().sum()/dataframe.shape[0]*100), 2)
    df_report["Tipo_dato"] = dataframe.dtypes
    return df_report

rom src.eda.soporte_eda import *