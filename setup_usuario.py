import os
import qrcode
import pyotp
from auth import crear_usuario


def crear_qr_2fa(username, secreto):
    os.makedirs("usuarios", exist_ok=True)

    uri = pyotp.totp.TOTP(secreto).provisioning_uri(
        name=username,
        issuer_name="Sistema BI Gasto Reactivacion"
    )

    img = qrcode.make(uri)
    ruta = f"usuarios/qr_2fa_{username}.png"
    img.save(ruta)

    return ruta


if __name__ == "__main__":
    print("CREACIÓN DE USUARIO ADMINISTRADOR")
    username = input("Usuario: ")
    nombre = input("Nombre completo: ")
    password = input("Contraseña: ")

    secreto = crear_usuario(username, password, nombre)
    ruta_qr = crear_qr_2fa(username, secreto)

    print("\nUsuario creado correctamente.")
    print("Escanea este QR con Google Authenticator o Microsoft Authenticator:")
    print(ruta_qr)
    print("\nSecreto 2FA:", secreto)