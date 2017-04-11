class Error(Exception):
    pass


class TabNotFoundError(Error):
    """
    Used when searching for a non-existent tab, using a certain username.
    """
    def __init__(self, username):
        self.message = ("Tab %s Not Found!", username)


class UsernameError(Error):
    """
    Used when the username:
        1) already exists
        2) is empty
        3) does not have a @ sign at the front
        4) has more than one @

    """
    def __init__(self, error):
        if error == 1:
            self.message = "Username already exists! Please enter a new username."
        elif error == 2:
            self.message = "No username entered! Please enter a valid username."
        elif error == 3:
            self.message = "Invalid username format! Please start with an @ sign."
        elif error == 4:
            self.message = "Username must be alphanumeric! Please enter a valid username."
        else:
            self.message = "Unknown Username Error"