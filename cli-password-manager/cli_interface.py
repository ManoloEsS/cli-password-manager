import argparse
import functions


def parser():
    parser = argparse.ArgumentParser(
        prog="clipm", description="a simple and secure password manager"
    )
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-a",
        "--add",
        help="will ask you for your username and password that goes with it",
        action="store_true",
    )
    group.add_argument(
        "-r",
        "--retrieve",
        help="will retrieve your password for the specified username or service",
        action="store_true",
    )
    group.add_argument(
        "-l",
        "--list",
        help="will list out all services and usernames",
        action="store_true",
    )
    group.add_argument(
        "-m",
        "--modify",
        help="Modify an existing password or delete a saved username password pair",
        action="store_true",
    )
    # group.add_argument(
    #     "-g",
    #     "--generate",
    #     help="will generate a password, then will ask for comfirmation of that password. Then will ask the service and username the password would be saved under",
    #     type=str,
    # )
    args = parser.parse_args()

    if args.add:
        functions.add_password()
    elif args.retrieve:
        functions.retrieve_password()
    elif args.list:
        functions.list_all()
    elif args.modify:
        functions.modify_remove_username()
