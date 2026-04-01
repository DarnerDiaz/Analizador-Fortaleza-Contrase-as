"""
Tests para el módulo de cifrado (encryption.py)
"""

import pytest
import os
import sys
from pathlib import Path

# Agregar ruta padre
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.encryption import PasswordEncryptor


class TestPasswordEncryptor:
    """Tests para el cifrado de contraseñas"""

    def test_derive_key_consistency(self):
        """Una misma contraseña y salt deben producir la misma clave"""
        master_password = "MyMasterPassword123!"
        salt = os.urandom(32)

        key1 = PasswordEncryptor.derive_key(master_password, salt)
        key2 = PasswordEncryptor.derive_key(master_password, salt)

        assert key1 == key2
        assert len(key1) == 32  # 256 bits

    def test_derive_key_different_salt(self):
        """Diferentes salts deben producir diferentes claves"""
        master_password = "MyMasterPassword123!"
        salt1 = os.urandom(32)
        salt2 = os.urandom(32)

        key1 = PasswordEncryptor.derive_key(master_password, salt1)
        key2 = PasswordEncryptor.derive_key(master_password, salt2)

        assert key1 != key2

    def test_encrypt_decrypt_simple(self):
        """Cifrar y descifrar debe devolver la misma contraseña"""
        password = "MySecurePassword123!"
        master_password = "MasterKey456789"

        encrypted = PasswordEncryptor.encrypt(password, master_password)
        decrypted = PasswordEncryptor.decrypt(encrypted, master_password)

        assert decrypted == password

    def test_encrypt_decrypt_complex_characters(self):
        """Debe manejar correctamente caracteres especiales y unicode"""
        password = "P@ss!w0rd#2024ñ$%&*()_+-=[]{}|;:',.<>?/~`"
        master_password = "MasterKey456789"

        encrypted = PasswordEncryptor.encrypt(password, master_password)
        decrypted = PasswordEncryptor.decrypt(encrypted, master_password)

        assert decrypted == password

    def test_encrypt_different_masters(self):
        """Diferentes master passwords deben producir diferentes cifrados"""
        password = "MySecurePassword123!"
        master1 = "MasterKey1"
        master2 = "MasterKey2"

        encrypted1 = PasswordEncryptor.encrypt(password, master1)
        encrypted2 = PasswordEncryptor.encrypt(password, master2)

        assert encrypted1 != encrypted2

    def test_decrypt_wrong_master_password(self):
        """Descifrar con contraseña maestra incorrecta debe llevar a datos inválidos"""
        password = "MySecurePassword123!"
        master_password = "CorrectMasterKey"
        wrong_password = "WrongMasterKey"

        encrypted = PasswordEncryptor.encrypt(password, master_password)
        
        # Intentar descifrar con contraseña incorrecta
        try:
            decrypted = PasswordEncryptor.decrypt(encrypted, wrong_password)
            # Si no levanta excepción, el resultado debe ser diferente
            assert decrypted != password
        except ValueError:
            # Si levanta excepción, eso es aceptable también
            pass

    def test_encrypt_empty_password(self):
        """Debe manejar contraseñas vacías correctamente"""
        password = ""
        master_password = "MasterKey456789"

        encrypted = PasswordEncryptor.encrypt(password, master_password)
        decrypted = PasswordEncryptor.decrypt(encrypted, master_password)

        assert decrypted == password

    def test_encrypt_very_long_password(self):
        """Debe manejar contraseñas muy largas"""
        password = "A" * 10000
        master_password = "MasterKey456789"

        encrypted = PasswordEncryptor.encrypt(password, master_password)
        decrypted = PasswordEncryptor.decrypt(encrypted, master_password)

        assert decrypted == password

    def test_encrypted_data_is_base64(self):
        """El dato cifrado debe ser válido base64"""
        import base64

        password = "MySecurePassword123!"
        master_password = "MasterKey456789"

        encrypted = PasswordEncryptor.encrypt(password, master_password)

        # Debe ser decodificable como base64
        try:
            base64.b64decode(encrypted)
            assert True
        except Exception:
            assert False, "Encrypted data is not valid base64"

    def test_encrypt_produces_different_ciphertexts(self):
        """Encriptar la misma contraseña debe producir diferentes resultados (por el IV)"""
        password = "MySecurePassword123!"
        master_password = "MasterKey456789"

        encrypted1 = PasswordEncryptor.encrypt(password, master_password)
        encrypted2 = PasswordEncryptor.encrypt(password, master_password)

        # Deben ser diferentes por el IV aleatorio
        assert encrypted1 != encrypted2

        # Pero deben descifrarse a lo mismo
        decrypted1 = PasswordEncryptor.decrypt(encrypted1, master_password)
        decrypted2 = PasswordEncryptor.decrypt(encrypted2, master_password)

        assert decrypted1 == password
        assert decrypted2 == password
