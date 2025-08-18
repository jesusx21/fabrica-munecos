from copy import deepcopy

from sqlalchemy.exc import NoResultFound

from ..errors import DatabaseError


class InvalidData(DatabaseError):
    def __init__(self, data: dict, error: Exception = None):
        info = deepcopy(data)

        super().__init__(
            error,
            'Invalid data received.',
            info
        )


class NotFound(DatabaseError):
    def __init__(self, record_name: str, query: dict, error: NoResultFound = None):
        info = deepcopy(query)
        info['record_name'] = record_name

        super().__init__(
            error,
            f'{record_name} was not found.',
            info
        )


class InvalidId(InvalidData):
    def __init__(self, id):
        super().__init__({ 'id': id })

        self.message = 'Id must be a UUID.'


class EmailAlreadyUsed(InvalidData):
    def __init__(self, email):
        super().__init__({ 'email': email })

        self.message = 'Email was already used.'


class ProfileNotFound(NotFound):
    def __init__(self, query, error = None):
        super().__init__('Profile', query, error)


class SessionNotFound(NotFound):
    def __init__(self, query, error = None):
        super().__init__('Session', query, error)


class UserNotFound(NotFound):
    def __init__(self, query, error = None):
        super().__init__('User', query, error)
