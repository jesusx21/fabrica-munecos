from datetime import datetime
from uuid import UUID

from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256

from hotties_factory.app.core import Entity
from hotties_factory.app.entities.errors import MissingPassword, InvalidPasswordValue, PasswordAlreadySet


class Password:
    def __init__(self, hash: str, salt: str):
        self.hash = hash
        self.salt = salt

    @staticmethod
    def encode(raw_password: str):
        password_salt = get_random_bytes(32).hex()
        password_hash = SHA256.new(data=str.encode(f'{raw_password}{password_salt}')) \
            .hexdigest()

        return Password(password_hash, password_salt)

    def does_match(self, raw_password: str):
        password_hash = SHA256.new(
            data=str.encode(f'{raw_password}{self.salt}')
        ).hexdigest()

        return self.hash == password_hash

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

    def add_password(self, raw_password: str = None, password: Password = None):
        if raw_password is None and password is None:
            raise MissingPassword()
        elif raw_password is not None and password is not None:
            raise InvalidPasswordValue()
        elif raw_password is not None and password is None:
            password = Password.encode(raw_password)

        self.password = password

    def does_password_match(self, raw_password: str):
        return self.password.does_match(raw_password)
