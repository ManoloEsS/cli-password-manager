from cryptography.fernet import Fernet
import base64
import hashlib
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from cryptography.hazmat.primitives import hashes


def make_lower_nospace(passkey):
    processed_key = "".join(passkey.lower().strip().split())
    return processed_key


def deterministic_salt(processed_passkey):
    return hashlib.sha256(processed_passkey.encode()).digest()[:16]


def encrypt(password, unprocessed_passkey):
    clean_passkey = make_lower_nospace(unprocessed_passkey)
    salt = deterministic_salt(clean_passkey)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(clean_passkey.encode("utf-8")))
    f = Fernet(key)
    encrypted_token = f.encrypt(password.encode("utf-8"))
    return base64.urlsafe_b64encode(encrypted_token).decode("utf-8")


def decrypt(encrypted_token, passkey):
    clean_passkey = make_lower_nospace(passkey)
    salt = deterministic_salt(clean_passkey)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(clean_passkey.encode("utf-8")))
    f = Fernet(key)
    encrypted_bytes = base64.urlsafe_b64decode(encrypted_token)
    decrypted_password = f.decrypt(encrypted_bytes).decode("utf-8")
    return decrypted_password


# TEST DELETE BEFORE SHIPPING
if __name__ == "__main__":
    paskey = input("please select 4 words: ")
    secret = input("Enter text to encrypt: ")
    encrypted = encrypt(paskey, secret)
    print("Encrypted:", encrypted)

    decrypted = decrypt(paskey, encrypted)
    print("Decrypted:", decrypted)
    print("Decrypted:", decrypted)
