import argparse
import getpass
import sys

def main():
    print("Hello from cli-password-manager!")
    parser = argparse.ArgumentParser(
        prog="password manager",
        description="a simple and secure password manager"
    )

    parser.add_argument(
        "-a","--add",
        help="will ask you for your username and password that goes with it",

    )
    parser.add_argument(
        "-r","--retrieve",
        help="will retrieve your password for the specified username or service",

    )
    parser.add_argument(
        "-l","--list",
        help="will list out all services and usernames",

    )
    parser.add_argument(
        "-g","--generate",
        help="will generate a password, then will ask for comfirmation of that password. Then will ask the service and username the password would be saved under",

    )
    #parser.add_argument(
    #   "--resetall",
    #    help="will reset your 4 encryption words but will delete all passwords in the process",
    #)
    args = parser.parse_args()

    #TEST PRINT DELETE BEFORE SHIPPING
    print("this works fine")

if __name__ == "__main__":
    main()
