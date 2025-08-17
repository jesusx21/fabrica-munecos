from uuid import UUID

from sqlalchemy.exc import IntegrityError, NoResultFound

from ..errors import EmailAlreadyUsed, InvalidId, UserNotFound
from .errors import SQLDatabaseError
from database.tables import Users
from hotties_factory.app.entities import User


class SQLUsersStore:
    def __init__(self, database):
        self._database = database

    async def create(self, user: User):
        statement = Users \
            .insert() \
            .values(
                names=user.names,
                last_names=user.last_names,
                email=user.email,
                password_hash=user.password.hash,
                password_salt=user.password.salt
            )

        try:
            cursor = await self._database.execute(statement)
        except IntegrityError as error:
            raise EmailAlreadyUsed(user.email) from error
        except Exception as error:
            raise SQLDatabaseError(error)

        user_id = cursor.inserted_primary_key[0]

        return await self.find_by_id(user_id)

    async def find_by_id(self, user_id: UUID):
        if not isinstance(user_id, UUID):
            raise InvalidId(user_id)

        statement = Users \
            .select() \
            .where(Users.c.id == user_id)

        try:
            cursor = await self._database.execute(statement)

            return self._create_user(cursor.one())
        except NoResultFound as error:
            raise UserNotFound({ 'id': user_id }) from error
        except Exception as error:
            raise SQLDatabaseError(error)

    def _create_user(self, cursor):
        user = User(
            id=cursor.id,
            names=cursor.names,
            last_names=cursor.last_names,
            email=cursor.email,
            created_at=cursor.created_at,
            updated_at=cursor.updated_at
        )

        user.set_password(cursor.password_hash, cursor.password_salt)

        return user
