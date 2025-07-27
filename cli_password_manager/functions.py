import os
from cli_password_manager import encryption
import json
import getpass
import string
import random
from pyfiglet import figlet_format


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
        user_name = input("Enter the username for the service: ").strip()
        if not user_name:
            print("Username cannot be empty.")
            continue

        if os.path.isfile(passwords_file) and os.path.getsize(passwords_file) > 0:
            with open(passwords_file, "r") as f:
                saved_passwords = json.load(f)
            if service in saved_passwords and user_name in saved_passwords[service]:
                print(
                    f"Username {user_name} for {service} already has a password stored."
                )
                overwrite = input("Overwrite? [y/n]").lower()
                if overwrite == "y":
                    break
                else:
                    print("Exiting program without overwriting.")
                    return
        break

    while True:
        password = getpass.getpass("Enter the password to be encrypted: \U0001f512")
        if not password:
            print("Password cannot be empty.")
            continue
        break
    while True:
        passkey = getpass.getpass(
            "Enter your 4 word key separated with a space: \U0001f512"
        )
        if len(passkey.strip().split()) != 4:
            print("Passkey must be exactly 4 words separated by spaces.")
            continue
        confirmation = getpass.getpass("Confirm your 4 word key: \U0001f512")
        if passkey != confirmation:
            print("Does not match. Please try again.")
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

    print(figlet_format("Password Added!", font="big"))


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
        print("Service not found. Saved services: ")
        for service in saved_passwords:
            print(service)
        service = input("Enter the name of the service: ")

    if saved_passwords[service]:
        print("Saved usernames for service are: ")
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
            passkey = getpass.getpass(
                "Enter your 4 word key separated with a space: \U0001f512"
            )
            decrypted_password = encryption.decrypt(encrypted_password, passkey)
            break
        except Exception:
            print("Incorrect passkey. Please try again or Ctrl+C to exit")
    try:
        print(f"Password for {user_name}: {decrypted_password}")
    except NameError:
        print("Failed to retrieve password. Please check your passkey and try again.")


def list_all():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    passwords_file = os.path.join(script_directory, "passwords.json")

    if not os.path.isfile(passwords_file) or os.path.getsize(passwords_file) == 0:
        print(
            "Passwords file doesn't exist or is empty. Add a password with the command 'clipm -a'"
        )
        return

    with open(passwords_file, "r") as f:
        saved_passwords = json.load(f)

    services_usernames_tree(saved_passwords)


def services_usernames_tree(data, prefix="", is_last=True):
    items = list(data.items())
    for index, (key, value) in enumerate(items):
        last = index == len(items) - 1
        connector = "└── " if last else "├── "
        print(prefix + connector + str(key))
        if isinstance(value, dict) and "password" not in value:
            extension = "    " if last else "│   "
            services_usernames_tree(value, prefix + extension, last)


def modify_remove_username():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    passwords_file = os.path.join(script_directory, "passwords.json")

    if not os.path.isfile(passwords_file) or os.path.getsize(passwords_file) == 0:
        print(
            "Passwords file doesn't exist or is empty. Add a password with the command 'clipm -a'"
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
        "Enter new password or leave empty to delete username: \U0001f512"
    )

    while True:
        passkey = getpass.getpass(
            "Enter your 4 word key separated with a space: \U0001f512"
        )
        if len(passkey.strip().split()) != 4:
            print("Passkey must be exactly 4 words separated by spaces.")
            continue
        break

    if new_password == "":
        del saved_passwords[service][user_name]
        if not saved_passwords[service]:
            del saved_passwords[service]
        with open(passwords_file, "w") as f:
            json.dump(saved_passwords, f, indent=4)
        print("Username/password succesfully deleted!")
        return

    new_encrypted_password = encryption.encrypt(new_password, passkey)
    saved_passwords[service][user_name]["password"] = new_encrypted_password

    with open(passwords_file, "w") as f:
        json.dump(saved_passwords, f, indent=4)

    print(figlet_format("Username/password succesfully modified!", font="big"))


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

    while True:
        password = ""
        for i in range(6):
            randomchar = random.choice(letters)
            password += randomchar
            randomnum = random.choice(numbers)
            password += randomnum
            randomspecial = random.choice(special_characters)
            password += randomspecial
        password_ok = input(f"Is {password} ok?[y/n]").lower()
        if password_ok == "y":
            break
    print(f"Generated secure password: {password}")


def reset():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    passwords_file = os.path.join(script_directory, "passwords.json")

    try:
        os.remove(passwords_file)
        print(
            "File succesfully deleted! Use 'clipm -a' to create a new file and store a password"
        )
    except FileNotFoundError:
        print(
            "Passwords file doesn't exist. Use 'clipm -a' to create a file and store a password"
        )
