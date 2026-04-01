"""
Módulo de cifrado AES-256 para almacenamiento seguro de contraseñas
"""

import os
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64


class PasswordEncryptor:
    """
    Gestiona cifrado y descifrado de contraseñas con AES-256-CBC
    """

    @staticmethod
    def derive_key(master_password: str, salt: bytes, iterations: int = 100000) -> bytes:
        """
        Deriva una clave a partir de la contraseña maestra usando PBKDF2

        Args:
            master_password: Contraseña maestra del usuario
            salt: Salt para la derivación
            iterations: Número de iteraciones PBKDF2

        Returns:
            Clave de 32 bytes (256 bits) para AES-256
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=iterations,
            backend=default_backend()
        )
        return kdf.derive(master_password.encode())

    @staticmethod
    def encrypt(password: str, master_password: str) -> str:
        """
        Cifra una contraseña con AES-256-CBC

        Args:
            password: Contraseña a cifrar
            master_password: Contraseña maestra para derivar la clave

        Returns:
            String con formato base64 que contiene: salt + iv + ciphertext
        """
        # Generar salt aleatorio
        salt = os.urandom(32)

        # Derivar clave
        key = PasswordEncryptor.derive_key(master_password, salt)

        # Generar IV aleatorio
        iv = os.urandom(16)

        # Cifrar
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()

        # Padding PKCS7
        plaintext = password.encode()
        block_size = 16
        padding_length = block_size - (len(plaintext) % block_size)
        padded_plaintext = plaintext + bytes([padding_length]) * padding_length

        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

        # Combinar: salt + iv + ciphertext y codificar en base64
        encrypted_data = salt + iv + ciphertext
        encoded = base64.b64encode(encrypted_data).decode('utf-8')

        return encoded

    @staticmethod
    def decrypt(encrypted_data: str, master_password: str) -> str:
        """
        Descifra una contraseña cifrada con AES-256-CBC

        Args:
            encrypted_data: String base64 con salt + iv + ciphertext
            master_password: Contraseña maestra para derivar la clave

        Returns:
            Contraseña descifrada

        Raises:
            ValueError: Si la descifración falla (contraseña maestra incorrecta)
        """
        try:
            # Decodificar base64
            encrypted_bytes = base64.b64decode(encrypted_data)

            # Extraer componentes
            salt = encrypted_bytes[:32]
            iv = encrypted_bytes[32:48]
            ciphertext = encrypted_bytes[48:]

            # Derivar clave
            key = PasswordEncryptor.derive_key(master_password, salt)

            # Descifrar
            cipher = Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()
            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

            # Remover padding PKCS7
            padding_length = padded_plaintext[-1]
            plaintext = padded_plaintext[:-padding_length]

            return plaintext.decode('utf-8')

        except Exception as e:
            raise ValueError("Error al descifrar: contraseña maestra incorrecta o datos corruptos") from e

    @staticmethod
    def save_credentials(credentials: dict, filepath: str, master_password: str):
        """
        Guarda credenciales cifradas en un archivo JSON

        Args:
            credentials: Diccionario con las credenciales
            filepath: Ruta del archivo
            master_password: Contraseña maestra
        """
        encrypted_creds = {}
        for key, password in credentials.items():
            encrypted_creds[key] = PasswordEncryptor.encrypt(password, master_password)

        with open(filepath, 'w') as f:
            json.dump(encrypted_creds, f, indent=2)

    @staticmethod
    def load_credentials(filepath: str, master_password: str) -> dict:
        """
        Carga credenciales cifradas desde un archivo JSON

        Args:
            filepath: Ruta del archivo
            master_password: Contraseña maestra

        Returns:
            Diccionario con las credenciales descifradas
        """
        with open(filepath, 'r') as f:
            encrypted_creds = json.load(f)

        decrypted_creds = {}
        for key, encrypted_password in encrypted_creds.items():
            decrypted_creds[key] = PasswordEncryptor.decrypt(encrypted_password, master_password)

        return decrypted_creds
