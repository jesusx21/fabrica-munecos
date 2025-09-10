from hotties_factory.app.errors import AppError


class EntityError(AppError): pass


class PasswordAlreadySet(EntityError):
    def __init__(self):
        super().__init__(message = 'Password was already set.')


class MissingPassword(EntityError):
    def __init__(self):
        super().__init__(message = 'Password value is missing.')



class InvalidPasswordValue(EntityError):
    def __init__(self):
        super().__init__(message = 'Just one value for password is valid.')
