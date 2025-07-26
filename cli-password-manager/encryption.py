from cryptography.fernet import Fernet
import base64
import hashlib
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


def make_lower_nospace(word):
    if not word.replace(" ", "").isalpha():
        print("Please enter only alphabetic characters and spaces.")
        return None
    word = word.lower().replace(" ", "")
    print(word)
    return word


def deterministic_salt(pw):
    return hashlib.sha256(pw.encode("utf-8")).digest()


def encrypt(passphrase, plaintext):
    clean_paskey = make_lower_nospace(passphrase)
    if clean_paskey is None:
        raise ValueError("Invalid passphrase")
    salt = deterministic_salt(clean_paskey)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(clean_paskey.encode("utf-8")))
    f = Fernet(key)
    token = f.encrypt(plaintext.encode("utf-8"))
    return token


def decrypt(passphrase, token):
    clean_paskey = make_lower_nospace(passphrase)
    if clean_paskey is None:
        raise ValueError("Invalid passphrase")
    salt = deterministic_salt(clean_paskey)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(clean_paskey.encode("utf-8")))
    f = Fernet(key)
    plaintext = f.decrypt(token).decode("utf-8")
    return plaintext


# TEST DELETE BEFORE SHIPPING
if __name__ == "__main__":
    paskey = input("please select 4 words: ")
    secret = input("Enter text to encrypt: ")
    encrypted = encrypt(paskey, secret)
    print("Encrypted:", encrypted)

    decrypted = decrypt(paskey, encrypted)
    print("Decrypted:", decrypted)
