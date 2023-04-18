"""
Main module to run the user management system.

This module imports the UserMenu class from the user_menu module
and creates an instance of it to run the user management system.
"""
from user_menu import UserMenu


def main():
    user_management_system = UserMenu()
    user_management_system.run()


if __name__ == "__main__":
    main()
