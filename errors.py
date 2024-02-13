class OutOfStockError(Exception):
    """Raised when the stock is not sufficient."""

    def __init__(self, message):
        super().__init__(message)


class Unauthorized(Exception):
    """Raised when the stock is not sufficient."""

    def __init__(self, message):
        super().__init__(message)



class ValueError(Exception):
    """Raised when the stock is not sufficient."""

    def __init__(self, message):
        super().__init__(message)
        
class FileError(Exception):
    """Raised when the stock is not sufficient."""

    def __init__(self, message):
        super().__init__(message)


class DatabaseError(Exception):
    """Raised when the stock is not sufficient."""

    def __init__(self, message):
        super().__init__(message)
