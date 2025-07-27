import os
import encryption
import json
import getpass
import string
import random


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

    print("Password added!")


def retrieve_password():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    passwords_file = os.path.join(script_directory, "passwords.json")

    if not os.path.isfile(passwords_file) or os.path.getsize(passwords_file) == 0:
        print(
            "Passwords file doesn't exist or is empty. Add a password with the command 'clipm -add'"
        )
        return

    while True:
        service = input("Enter the name of the service: ").strip()
        if not service:
            print("Service name cannot be empty.")
            continue
        break

    with open(passwords_file, "r") as f:
        saved_passwords = json.load(f)

    while service not in saved_passwords:
        service_completions = trie(service[0])
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

    while True:
        try:
            encrypted_password = saved_passwords[service][user_name]["password"]
            passkey = getpass.getpass("Enter your 4 word key separated with a space: ")
            decrypted_password = encryption.decrypt(encrypted_password, passkey)
            break
        except Exception:
            print("Incorrect passkey. Please try again or Ctrl+C to exit")
    print(f"Password for {user_name}: {decrypted_password}")


def list_all():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    passwords_file = os.path.join(script_directory, "passwords.json")

    if not os.path.isfile(passwords_file) or os.path.getsize(passwords_file) == 0:
        print(
            "Passwords file doesn't exist or is empty. Add a password with the command 'clipm -add'"
        )
        return

    with open(passwords_file, "r") as f:
        saved_passwords = json.load(f)

    services_usernames_tree(saved_passwords)


def services_usernames_tree(data, indent=0):
    for key, value in data.items():
        print(" " * indent + key)
        if isinstance(value, dict) and "password" not in value:
            services_usernames_tree(value, indent + 4)


def modify_remove_username():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    passwords_file = os.path.join(script_directory, "passwords.json")

    if not os.path.isfile(passwords_file) or os.path.getsize(passwords_file) == 0:
        print(
            "Passwords file doesn't exist or is empty. Add a password with the command 'clipm -add'"
        )
        return

    with open(passwords_file, "r") as f:
        saved_passwords = json.load(f)

    service = input("Enter name of the service: ")
    while service not in saved_passwords:
        service_completions = trie(service[0])
        print("Service not found. Similar service names: ")
        for service in service_completions:
            print(service)
        service = input("Enter the name of the service: ")

    user_name = input("Enter a username to modify: ")
    while user_name not in saved_passwords[service]:
        print("Username not found. Saved usernames are: ")
        for username in saved_passwords[service].keys():
            print(username)
        user_name = input("Enter a valid username: ")

        new_password = getpass.getpass(
            "Enter new password or leave empty to delete username: "
        )

    while True:
        passkey = getpass.getpass("Enter your 4 word key separated with a space: ")
        if len(passkey.strip().split()) != 4:
            print("Passkey must be exactly 4 words separated by spaces.")
            continue
        break

    password_to_modify = getpass.getpass("Enter the old password: ")
    encrypted_old_password = saved_passwords[service][user_name]["password"]
    password_check = encryption.encrypt(password_to_modify, passkey)

    while password_check != encrypted_old_password:
        password_to_modify = getpass.getpass("Wrong password. Try again: ")
        password_check = encryption.encrypt(password_to_modify, passkey)

    if not new_password:
        del saved_passwords[service][user_name]
        if not saved_passwords[service]:
            del saved_passwords[service]
        return

    new_encrypted_password = encryption.encrypt(new_password, passkey)
    saved_passwords[service][user_name]["password"] = new_encrypted_password

    with open(passwords_file, "w") as f:
        json.dump(saved_passwords, f, indent=4)

    print("Username/password succesfully modified!")


def trie(prefix):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    passwords_file = os.path.join(script_directory, "passwords.json")

    if not os.path.isfile(passwords_file) or os.path.getsize(passwords_file) == 0:
        return []

    with open(passwords_file, "r") as f:
        saved_passwords = json.load(f)

    return [service for service in saved_passwords if service.startswith(prefix)]


def generate():
    letters = string.ascii_letters
    numbers = string.digits
    special_characters = string.punctuation

    all_characters = letters + numbers + special_characters
    password = ""
    for i in range(17):
        randomchar = random.choice(all_characters)
        password += randomchar
    print(password)
