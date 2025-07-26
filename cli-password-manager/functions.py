import os
import encryption
import json


def add_password(password: str, user_name: str, service: str):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    passwords_file = os.path.join(script_directory, "passwords.json")
    encrypted_password = encryption.encrypt(password)

    if not os.path.isfile(passwords_file):
        with open(passwords_file, "w") as f:
            json.dump({}, f)
        print(f"File created at: {passwords_file}")

    if os.path.getsize(passwords_file) > 0:
        with open(passwords_file, "r") as f:
            saved_passwords = json.load(f)
    else:
        saved_passwords = {}

    if service not in saved_passwords:
        saved_passwords[service] = {}

    saved_passwords[service][user_name] = {"password": encrypted_password}

    with open(passwords_file, "w") as f:
        json.dump(saved_passwords, f, indent=4)
