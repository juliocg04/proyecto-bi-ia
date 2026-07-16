import sqlite3
import pandas as pd
import os


def obtener_ruta_base():
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(carpeta_actual, "bd_gasto_reactivacion.db")


def obtener_conexion():
    ruta_db = obtener_ruta_base()
    return sqlite3.connect(ruta_db)


def ejecutar_consulta(query):
    conexion = obtener_conexion()
    df = pd.read_sql_query(query, conexion)
    conexion.close()
    return df