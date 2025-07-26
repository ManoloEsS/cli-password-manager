import os
import encryption
import json
import getpass


def add_password():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    passwords_file = os.path.join(script_directory, "passwords.json")

    service = input("Enter the name of the service: ")
    user_name = input("Enter your username for the service")
    password = getpass.getpass("Enter the password to be encrypted: ")
    passkey = getpass.getpass("Enter your 4 word key separated with a space: ")

    encrypted_password = encryption.encrypt(password, passkey)

    if not os.path.isfile(passwords_file):
        with open(passwords_file, "w") as f:
            json.dump({}, f)

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


def retrieve_password():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    passwords_file = os.path.join(script_directory, "passwords.json")

    if not os.path.isfile(passwords_file):
        print(
            "Passwords file doesn't exist. Add a password with the command 'clipm -add'"
        )
        return

    if os.path.getsize(passwords_file) == 0:
        print("Passwords file is empty. Add a password with the command 'clipm -add'")
        return

    service = input("Enter the name of the service: ")

    with open(passwords_file, "r") as f:
        saved_passwords = json.load(f)

    while service not in saved_passwords:
        completions = trie(service)
        print("Service not found. Similar service names: ")
        for service in completions:
            print(service)
        service = input("Enter the name of the service: ")

    for key in saved_passwords[service].keys():
        print(key)

    user_name = input("Enter the username: ")
    encrypted_password = saved_passwords[service][user_name]["password"]
    passkey = getpass.getpass("Enter your 4 word key separated with a space: ")
    decrypted_password = encryption.decrypt(encrypted_password, passkey)
    print(decrypted_password)


def list_all():
    pass


def show_help():
    pass


def trie():
    pass
