class OutOfStockError(Exception):
    """Raised when the stock is not sufficient."""

    def __init__(message):
        super().__init__(message)
