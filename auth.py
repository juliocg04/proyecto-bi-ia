import sqlite3
import bcrypt


DB = "bd_gasto_reactivacion.db"


def obtener_conexion():
    return sqlite3.connect(DB)


def crear_tabla_usuarios():
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios_sistema (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            usuario TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            rol TEXT NOT NULL DEFAULT 'ADMIN',
            activo INTEGER NOT NULL DEFAULT 1
        )
    """)

    conn.commit()
    conn.close()


def validar_login(usuario, clave):
    crear_tabla_usuarios()

    if not usuario or not clave:
        return False

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            password_hash,
            rol,
            activo
        FROM usuarios_sistema
        WHERE usuario = ?
    """, (usuario,))

    resultado = cursor.fetchone()
    conn.close()

    if resultado is None:
        return False

    password_hash, rol, activo = resultado

    if activo != 1:
        return False

    if rol != "ADMIN":
        return False

    try:
        return bcrypt.checkpw(
            clave.encode("utf-8"),
            password_hash.encode("utf-8")
        )
    except Exception:
        return False


def obtener_usuario(usuario):
    crear_tabla_usuarios()

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            usuario,
            nombre,
            correo,
            rol,
            activo
        FROM usuarios_sistema
        WHERE usuario = ?
    """, (usuario,))

    resultado = cursor.fetchone()
    conn.close()

    if resultado is None:
        return {
            "usuario": "",
            "nombre": "",
            "correo": "",
            "rol": "",
            "activo": 0
        }

    return {
        "usuario": resultado[0],
        "nombre": resultado[1],
        "correo": resultado[2],
        "rol": resultado[3],
        "activo": resultado[4]
    }