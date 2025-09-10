class AppError(Exception):
    DEFAULT_MESSAGE = 'Something unexpected happened'

    def __init__(self, error: Exception = None, message: str = DEFAULT_MESSAGE, info: dict = {}):
        super().__init__()

        self.cause = error
        self.message = message
        self.info = info


class EmailAlreadyRegistered(AppError):
    def __init__(self, email: str):
        super().__init__(
            message='Email provided was already used.',
            info={ 'email': email }
        )


class CouldNotRegisteredUser(AppError):
    def __init__(self, error: Exception):
        super().__init__(
            error=error,
            message='Something unexpected happened while registering user.'
        )
