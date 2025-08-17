class EntityError(Exception):
    DEFAULT_MESSAGE = 'Something unexpected happened'

    def __init__(self, error: Exception = None, message: str = DEFAULT_MESSAGE, info: dict = {}):
        super().__init__()

        self.cause = error
        self.message = message
        self.info = info


class PasswordAlreadySet(EntityError):
    def __init__(self):
        super().__init__(message = 'Password was already set')
