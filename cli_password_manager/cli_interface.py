import argparse
from cli_password_manager import functions
from pyfiglet import figlet_format
import sys


def parser():
    if "-h" in sys.argv or "--help" in sys.argv:
        (print(figlet_format("CLIPM", font="isometric1")),)
    parser = argparse.ArgumentParser(
        prog="clipm",
        description="""Cli-password-manager is a utility to encrypt, store and manage passwords from anywhere in your terminal.
        It allows you to have full control of your services' usernames and passwords by storing them locally and encrypted using a passkey of your choice.""",
    )
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-a",
        "--add",
        help="create a .json file and store an encrypted password tied to a service and username",
        action="store_true",
    )
    group.add_argument(
        "-r",
        "--retrieve",
        help="decrypt and retrieve a password for the specified service and username",
        action="store_true",
    )
    group.add_argument(
        "-l",
        "--list",
        help="list out all stored services and their usernames",
        action="store_true",
    )
    group.add_argument(
        "-m",
        "--modify",
        help="modify or delete an existing username-password pair",
        action="store_true",
    )
    group.add_argument(
        "-g",
        "--generate",
        help="generate a secure password",
        action="store_true",
    )
    group.add_argument(
        "-x",
        "--reset",
        help="delete .json file (use if encountering errors)",
        action="store_true",
    )
    args = parser.parse_args()

    if args.add:
        functions.add_password()
    elif args.retrieve:
        functions.retrieve_password()
    elif args.list:
        functions.list_all()
    elif args.modify:
        functions.modify_remove_username()
    elif args.generate:
        functions.generate()
