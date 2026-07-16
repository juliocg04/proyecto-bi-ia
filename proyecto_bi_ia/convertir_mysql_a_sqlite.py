import mysql.connector
import pandas as pd
import sqlite3

MYSQL_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "Soldierjesus2026@**",
    "database": "bd_gasto_reactivacion"
}

SQLITE_DB = "bd_gasto_reactivacion.db"

tablas = [
    "dim_tiempo",
    "dim_nivel_gobierno",
    "dim_sector",
    "dim_ubigeo",
    "dim_financiamiento",
    "hecho_gasto_reactivacion"
]

mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
sqlite_conn = sqlite3.connect(SQLITE_DB)

for tabla in tablas:
    print(f"Exportando tabla: {tabla}")
    df = pd.read_sql(f"SELECT * FROM {tabla}", mysql_conn)
    df.to_sql(tabla, sqlite_conn, if_exists="replace", index=False)

mysql_conn.close()
sqlite_conn.close()

print("Base SQLite creada correctamente:", SQLITE_DB)