import re


class User:
    """
    Represents a user in the user management system.

    Attributes:
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        age (int): The user's age.
        income (float): The user's income.
    """
    def __init__(self, first_name, last_name, age, income):
        """
        Constructs a new user object with the given attributes.

        Args:
            first_name (str): The user's first name.
            last_name (str): The user's last name.
            age (int): The user's age.
            income (float): The user's income.

        Raises:
            ValueError: If any of the arguments are invalid.
        """
        self.set_first_name(first_name)
        self.set_last_name(last_name)
        self.set_age(age)
        self.set_income(income)

    def get_first_name(self):
        """
        Returns the user's first name.

        Returns:
            str: The user's first name.
        """
        return self.first_name

    def set_first_name(self, first_name):
        """
        Sets the user's first name.

        Args:
            first_name (str): The user's first name.

        Raises:
            ValueError: If the first name is invalid.
        """
        if not isinstance(first_name, str):
            raise ValueError("First name must be a string.")
        # Allow letters, hyphens, and spaces
        if not re.match(r'^[A-Za-z -]+$', first_name):
            raise ValueError("First name must contain only alphabetical characters, hyphens, and spaces.")
        first_name = first_name.strip().title()
        self.first_name = first_name

    def get_last_name(self):
        """
        Returns the user's last name.

        Returns:
            str: The user's last name.
        """
        return self.last_name

    def set_last_name(self, last_name):
        """
        Sets the user's last name.

        Args:
            last_name (str): The user's last name.

        Raises:
            ValueError: If the last name is invalid.
        """
        if not isinstance(last_name, str):
            raise ValueError("Last name must be a string.")
        # Allow letters, hyphens, and spaces
        if not re.match(r'^[A-Za-z -]+$', last_name):
            raise ValueError("Last name must contain only alphabetical characters, hyphens, and spaces.")
        last_name = last_name.strip().title()
        self.last_name = last_name

    def get_age(self):
        """
        Returns the user's age.

        Returns:
            int: The user's age.
        """
        return self.age

    def set_age(self, age):
        """
        Sets the user's age.

        Args:
            age (int): The user's age.

        Raises:
            ValueError: If the age is invalid.
        """
        if not isinstance(age, int):
            raise ValueError("Age must be an integer.")
        if age < 1 or age > 125:
            raise ValueError("Age must be between 1 and 125.")
        self.age = age

    def get_income(self):
        """
        Returns the user's income.

        Returns:
            float: The user's income.
        """
        return self.income

    def set_income(self, income):
        """
        Sets the income of the user.

        Args:
            income (float): The income of the user. Must be a floating-point number between 10,000.50 and 500,000.75.

        Raises:
            ValueError: If income is not a floating-point number, or if it is not within the valid range.
        """
        if not isinstance(income, float):
            raise ValueError("Income must be a floating-point number.")
        if income < 10000.50 or income > 500000.75:
            raise ValueError("Income must be between 10,000.50 and 500,000.75.")
        self.income = income

