from cryptography.fernet import Fernet
import os
import base64


def _load_key() -> bytes:
    key = os.environ.get("ENCRYPTION_KEY")
    
    if not key:
        raise RuntimeError("ENCRYPTION_KEY is not set in environment variables")
    
    try:
        base64.urlsafe_b64decode(key)
    except Exception:
        raise RuntimeError("ENCRYPTION_KEY is not a valid Fernet key")
    
    return key.encode()

_fernet = Fernet(_load_key())


def encrypt(value: str) -> str:
    return _fernet.encrypt(value.encode()).decode()


def decrypt(value: str) -> str:
    return _fernet.decrypt(value.encode()).decode()


def generate_key() -> str:
    return Fernet.generate_key().decode()
