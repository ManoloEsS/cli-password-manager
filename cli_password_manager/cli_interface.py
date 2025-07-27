import argparse
from cli_password_manager import functions
from pyfiglet import figlet_format
import sys


def parser():
    if "-h" in sys.argv or "--help" in sys.argv:
        (print(figlet_format("CLIPM", font="isometric1")),)
    parser = argparse.ArgumentParser(
        prog="clipm", description="a simple and secure password manager"
    )
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-a",
        "--add",
        help="Ask you for your username and password that goes with it",
        action="store_true",
    )
    group.add_argument(
        "-r",
        "--retrieve",
        help="Retrieve your password for the specified username or service",
        action="store_true",
    )
    group.add_argument(
        "-l",
        "--list",
        help="List out all services and usernames",
        action="store_true",
    )
    group.add_argument(
        "-m",
        "--modify",
        help="Modify an existing password or delete a saved username password pair",
        action="store_true",
    )
    group.add_argument(
        "-g",
        "--generate",
        help="Generate a password",
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
