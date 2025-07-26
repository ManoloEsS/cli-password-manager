import os
import encryption
import json
import getpass


def add_password():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    passwords_file = os.path.join(script_directory, "passwords.json")

    while True:
        service = input("Enter the name of the service: ").strip()
        if not service:
            print("Service name cannot be empty.")
            continue
        break
    while True:
        user_name = input("Enter the user_name for the service: ").strip()
        if not user_name:
            print("Username cannot be empty.")
            continue
        break
    while True:
        password = getpass.getpass("Enter the password to be encrypted: ")
        if not password:
            print("Password cannot be empty.")
            continue
        break
    while True:
        passkey = getpass.getpass("Enter your 4 word key separated with a space: ")
        if len(passkey.strip().split()) != 4:
            print("Passkey must be exactly 4 words separated by spaces.")
            continue
        break

    # add error handling
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

    while True:
        service = input("Enter the name of the service: ").strip()
        if not service:
            print("Service name cannot be empty.")
            continue
        break

    service = input("Enter the name of the service: ")

    with open(passwords_file, "r") as f:
        saved_passwords = json.load(f)

    while service not in saved_passwords:
        service_completions = trie(service)
        print("Service not found. Similar service names: ")
        for service in service_completions:
            print(service)
        service = input("Enter the name of the service: ")

    for key in saved_passwords[service].keys():
        print(key)

    user_name = input("Enter a username: ")

    while user_name not in saved_passwords[service]:
        print("Username not found. Saved usernames are: ")
        for username in saved_passwords[service].keys():
            print(username)
        user_name = input("Enter a username: ")

    encrypted_password = saved_passwords[service][user_name]["password"]
    passkey = getpass.getpass("Enter your 4 word key separated with a space: ")
    decrypted_password = encryption.decrypt(encrypted_password, passkey)
    print(decrypted_password)


def list_all():
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

    with open(passwords_file, "r") as f:
        saved_passwords = json.load(f)

    services_usernames_tree(saved_passwords)


def services_usernames_tree(data, indent=0):
    for key, value in data.items():
        print(" " * indent + key)
        if isinstance(value, dict) and "password" not in value:
            services_usernames_tree(value, indent + 4)


def show_help():
    pass


def trie():
    pass
