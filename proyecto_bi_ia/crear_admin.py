import sqlite3
import bcrypt


DB = "bd_gasto_reactivacion.db"


def crear_tabla_usuarios():
    conn = sqlite3.connect(DB)
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


def crear_admin():
    print("=== CREAR USUARIO ADMINISTRADOR ===")

    nombre = input("Nombre completo: ").strip()
    correo = input("Correo: ").strip()
    usuario = input("Usuario: ").strip()
    clave = input("Contraseña: ").strip()

    if not nombre or not correo or not usuario or not clave:
        print("Todos los campos son obligatorios.")
        return

    password_hash = bcrypt.hashpw(
        clave.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO usuarios_sistema (
                nombre,
                correo,
                usuario,
                password_hash,
                rol,
                activo
            )
            VALUES (?, ?, ?, ?, 'ADMIN', 1)
        """, (nombre, correo, usuario, password_hash))

        conn.commit()
        print("Usuario administrador creado correctamente.")

    except sqlite3.IntegrityError:
        print("Error: el usuario o correo ya existe.")

    finally:
        conn.close()


if __name__ == "__main__":
    crear_tabla_usuarios()
    crear_admin()