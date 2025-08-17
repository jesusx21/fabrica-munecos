from datetime import datetime
from uuid import UUID

from .errors import PasswordAlreadySet
from hotties_factory.app.core import Entity


class Password:
    def __init__(self, hash: str, salt: str):
        self.hash = hash
        self.salt = salt


class User(Entity):
    def __init__(
        self,
        names: str,
        last_names: str,
        email: str,
        id: UUID = None,
        password: Password = None,
        created_at: datetime = None,
        updated_at: datetime = None
    ):
        super().__init__(id, created_at, updated_at)

        self.names = names
        self.last_names = last_names
        self.email = email
        self.password = password

    def set_password(self, hash: str, salt: str):
        if self.password is not None:
            raise PasswordAlreadySet()

        self.password = Password(hash, salt)
