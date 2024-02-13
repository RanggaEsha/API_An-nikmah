class Unauthorized(Exception):
    """
    Exception raised when an unauthorized access is attempted.

    Args:
        message (str): The error message to be displayed.
    """
    def __init__(self, message):
        super().__init__(message)

class ValueError(Exception):
    """
    Exception raised for invalid input values.

    Args:
        message (str): The error message to be displayed.
    """
    def __init__(self, message):
        super().__init__(message)

class FileError(Exception):
    """
    Exception raised for file-related errors.

    Args:
        message (str): The error message to be displayed.
    """
    def __init__(self, message):
        super().__init__(message)

class DatabaseError(Exception):
    """
    Exception raised for database-related errors.

    Args:
        message (str): The error message to be displayed.
    """
    def __init__(self, message):
        super().__init__(message)
