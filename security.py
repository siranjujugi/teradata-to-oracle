from cryptography.fernet import Fernet
from config import ENCRYPTION_KEY_PATH

def generate_key():
    key = Fernet.generate_key()
    ENCRYPTION_KEY_PATH.write_bytes(key)
    print("Key generated and saved to secret.key")

def encrypt_password(password: str) -> bytes:
    key = ENCRYPTION_KEY_PATH.read_bytes()
    fernet = Fernet(key)
    return fernet.encrypt(password.encode())

def decrypt_password(encrypted_password: bytes) -> str:
    key = ENCRYPTION_KEY_PATH.read_bytes()
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_password).decode()
