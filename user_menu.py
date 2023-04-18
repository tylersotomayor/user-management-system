from tkinter import *
from tkinter import messagebox, simpledialog
import os
from user import User
import re


class UserMenu:
    """
        This class represents a user menu that allows users to add, view, search, and delete user data.
        """
    def __init__(self):
        """
            A graphical user interface for managing user data.

            Attributes:
                user_list (list): A list of User objects representing the users in the system.
                file_path (str): The path to the file where user data is stored.
            """
        self.user_list = []
        self.file_path = 'user_data.txt'
        self.load_user_data()

    def load_user_data(self):
        """
        Loads user data from a file and populates the user list.

        Raises:
            Exception: If an error occurs while loading the data.
        """
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    for line in f:
                        data = line.strip().split(',')
                        first_name, last_name, age, income = data
                        age = int(age)
                        income = float(income)
                        user = User(first_name, last_name, age, income)
                        self.user_list.append(user)
        except Exception as e:
            self.show_error("Error Loading Data", f"An error occurred while loading user data: {str(e)}")

    def save_user_data(self):
        """
        Saves the user data to a file.

        The user data is saved to a file named 'user_data.txt' in the current working directory.
        If the file already exists, its contents will be overwritten.

        Raises:
            IOError: If there is an error writing to the file.
        """
        try:
            with open(self.file_path, 'w') as f:
                for user in self.user_list:
                    f.write(f"{user.first_name},{user.last_name},{user.age},{user.income}\n")
        except Exception as e:
            self.show_error("Error Saving Data", f"An error occurred while saving user data: {str(e)}")

    def run(self):
        """
        Runs the user management system.

        This method displays a main menu with options for adding users, viewing users, searching for users,
        deleting users, and quitting the program. The user is prompted to select an option from the menu,
        and the corresponding action is performed. The program continues to display the menu and perform
        actions until the user chooses to quit the program.

        Raises:
            ValueError: If the user enters an invalid choice from the menu.
        """
        ws = Tk()
        ws.withdraw()

        while True:
            choice = self.get_choice()
            if choice == 'A':
                self.add_user()
            elif choice == 'V':
                self.view_users()
            elif choice == 'S':
                self.search_users()
            elif choice == 'D':
                self.delete_user()
            elif choice == 'Q':
                self.save_user_data()  # save user data before quitting
                self.show_text("Quitting the program", "Have a nice day")
                break
            else:
                self.show_error("ERROR", "YOU MUST SELECT FROM THE MENU")

    MENU_OPTIONS = {
        'A': 'Add user',
        'V': 'View users',
        'S': 'Search users',
        'D': 'Delete user',
        'Q': 'Quit'
    }

    def get_choice(self):
        """
        Displays a menu of options to the user and returns the user's choice.

        Returns:
            str: The user's choice, represented by a single character.
        """
        main_menu = ""
        for key, value in self.MENU_OPTIONS.items():
            main_menu += f"[{key}] {value}\n"
        title = 'Main Menu'
        result = self.get_text(title, main_menu)
        if result is None:
            return 'Q'
        return result.upper()

    def add_user(self):
        """
        Prompts the user to enter data for a new user and adds the user to the user_list attribute.
        """
        while True:
            try:
                first_name = self.get_text("First Name", "Enter first name:", name_validation=True)
                if first_name is None:
                    break
                last_name = self.get_text("Last Name", "Enter last name:", name_validation=True)
                if last_name is None:
                    break
                age = self.get_int("Age", "Enter age:", 1, 125)
                if age is None:
                    break
                income = self.get_float("Annual Income", "Enter annual income:", 10000.50, 500000.75)
                if income is None:
                    break
                user = User(first_name, last_name, age, income)
                self.user_list.append(user)
                self.show_text("User Added", f"{first_name} {last_name} has been added to the user list.")
                break
            except ValueError as e:
                self.show_error("Input Error", str(e))

    def view_users(self):
        """
            Displays a list of users in the system in pages.

            If there are no users, a message is displayed indicating so.
            Otherwise, the users are displayed in pages of 20. The user can navigate through the pages
            using the options [P] for previous page, [N] for next page, and [X] to exit.

            Returns:
                None
        """
        if len(self.user_list) == 0:
            self.show_text("No Users", "There are no users to display.")
        else:
            users_per_page = 20
            num_pages = (len(self.user_list) + users_per_page - 1) // users_per_page
            current_page = 0

            while True:
                title = f"USER LIST - PAGE {current_page + 1}/{num_pages}"
                mess = ""
                for i in range(current_page * users_per_page,
                               min((current_page + 1) * users_per_page, len(self.user_list))):
                    user = self.user_list[i]
                    mess += f"{user.first_name} {user.last_name} - Age: {user.age}, Annual Income: ${user.income:,.2f}\n"

                mess += "\n[P] Previous Page [N] Next Page [X] Exit"
                result = self.get_text(title, mess)
                if result is None:  # User clicked "Cancel"
                    break
                elif result.upper() == 'P' and current_page > 0:
                    current_page -= 1
                elif result.upper() == 'N' and current_page < num_pages - 1:
                    current_page += 1
                else:
                    break

    def get_int(self, title, prompt, low=0, high=500, initial=None):
        """
            Gets an integer input from the user.

            Prompts the user with the given title and prompt, and requires the input to be an integer
            between the given low and high values.

            Args:
                title (str): The title of the input window.
                prompt (str): The prompt message to display to the user.
                low (int): The minimum value the input can have. Defaults to 0.
                high (int): The maximum value the input can have. Defaults to 500.
                initial (int): The initial value to display in the input field. Defaults to None.

            Returns:
                int or None: The integer inputted by the user, or None if the user cancels the input window.
        """
        while True:
            result = simpledialog.askinteger(title, prompt, minvalue=low, maxvalue=high, initialvalue=initial)
            if result is not None:
                try:
                    if low <= result <= high:
                        return result
                    else:
                        raise ValueError(f"Value must be between {low} and {high}.")
                except ValueError as e:
                    self.show_error("Input Error", str(e))
            else:
                return None

    def get_float(self, title, prompt, low=0.0, high=5000000.99, initial=None):
        """
        Gets a float input from the user.

        Prompts the user with the given title and prompt, and requires the input to be a float
        between the given low and high values.

        Args:
            title (str): The title of the input window.
            prompt (str): The prompt message to display to the user.
            low (float): The minimum value the input can have. Defaults to 0.0.
            high (float): The maximum value the input can have. Defaults to 5000000.99.
            initial (float): The initial value to display in the input field. Defaults to None.

        Returns:
            float or None: The float inputted by the user, or None if the user cancels the input window.
        """
        while True:
            result = simpledialog.askfloat(title, prompt, minvalue=low, maxvalue=high, initialvalue=initial)
            if result is not None:
                try:
                    if low <= result <= high:
                        return result
                    else:
                        raise ValueError(f"Value must be between {low} and {high}.")
                except ValueError as e:
                    self.show_error("Input Error", str(e))
            else:
                return None

    def get_text(self, title, prompt, show='', name_validation=False):
        """
        Gets a text input from the user.

        Prompts the user with the given title and prompt, and requires the input to be a non-empty string.
        If name_validation is True, the input must also only contain alphabetical characters, hyphens,
        and spaces.

        Args:
            title (str): The title of the input window.
            prompt (str): The prompt message to display to the user.
            show (str): The initial value to display in the input field. Defaults to an empty string.
            name_validation (bool): Whether to validate the input as a name. Defaults to False.

        Returns:
            str or None: The string inputted by the user, or None if the user cancels the input window.
        """
        while True:
            result = simpledialog.askstring(title, prompt, show=show)
            if result is not None:
                try:
                    if result.strip():
                        if name_validation:
                            if not re.match(r'^[A-Za-z -]+$', result):
                                raise ValueError("Name must contain only alphabetical characters, hyphens, and spaces.")
                        return result.strip()
                    else:
                        raise ValueError("Input cannot be empty.")
                except ValueError as e:
                    self.show_error("Input Error", str(e))
            else:
                return None

    def show_error(self, title, prompt):
        """
        Displays an error message box with the given title and prompt.

        Args:
            title (str): The title of the error message box.
            prompt (str): The error message to display.

        Returns:
            None
        """
        messagebox.showerror(title, prompt)

    def show_text(self, title, prompt):
        """
        Displays an information message box with the given title and prompt.

        Args:
            title (str): The title of the information message box.
            prompt (str): The message to display.

        Returns:
            None
        """
        messagebox.showinfo(title, prompt)

    def search_users(self):
        """
            Searches for users based on a given search term.

            The user is prompted to enter a search term, which can be either the first name,
            last name, or both. The method then searches the user list for matches and displays
            the results to the user. If there are no matches, a message is displayed saying so.
            If the search is cancelled, a message is displayed saying so.
        """
        search_term = self.get_text("Search Users", "Enter first name, last name, or both to search:")
        if search_term:
            search_results = [user for user in self.user_list if search_term.lower() in f"{user.first_name.lower()} {user.last_name.lower()}"]
            if search_results:
                title = "Search Results"
                message = ""
                for user in search_results:
                    message += f"{user.first_name} {user.last_name} - Age: {user.age}, Annual Income: ${user.income:,.2f}\n"
                self.show_text(title, message)
            else:
                self.show_text("No Matches", "No users found matching your search criteria.")
        else:
            self.show_text("Search Cancelled", "User search was cancelled.")

    def delete_user(self):
        """
            Deletes a user from the user list.

            The method first calls the `search_users` method to prompt the user to search for a
            user to delete. Then, the user is prompted to enter the full name of the user they want
            to delete. If the specified user is found, a confirmation message is displayed to the
            user, and the user is removed from the user list if they confirm. If the user does not
            confirm, a message is displayed saying so. If the specified user is not found, a message
            is displayed saying so. If the deletion is cancelled, a message is displayed saying so.
        """
        self.search_users()
        selected_user_name = self.get_text("Select User to Delete", "Enter the full name of the user you want to delete:")
        if selected_user_name:
            selected_user = None
            for user in self.user_list:
                if f"{user.first_name} {user.last_name}".lower() == selected_user_name.lower():
                    selected_user = user
                    break

            if selected_user:
                confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {selected_user.first_name} {selected_user.last_name}?")
                if confirm:
                    self.user_list.remove(selected_user)
                    self.show_text("User Deleted", f"{selected_user.first_name} {selected_user.last_name} "
                                                   f"has been deleted from the user list.")
                else:
                    self.show_text("Delete Cancelled", "User deletion was cancelled.")
            else:
                self.show_text("User Not Found", "The specified user was not found.")
        else:
            self.show_text("Delete Cancelled", "User deletion was cancelled.")

