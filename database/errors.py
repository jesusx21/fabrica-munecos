class DatabaseError(Exception):
    DEFAULT_MESSAGE = 'Something unexpected happened'

    def __init__(self, error: Exception = None, message: str = DEFAULT_MESSAGE, info: dict = {}):
        super().__init__()

        self.cause = error
        self.message = message
        self.info = info


class DatabaseDriverNotSupported(DatabaseError):
    def __init__(self, driver: str):
        super().__init__(info = { 'driver': driver })
