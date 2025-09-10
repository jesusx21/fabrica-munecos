from uuid import UUID

from sqlalchemy.exc import IntegrityError, NoResultFound

from database.tables import Users
from hotties_factory.app.entities import Password, User
from hotties_factory.database.stores.errors import EmailAlreadyUsed, InvalidId, UserNotFound
from hotties_factory.database.stores.sql.errors import SQLDatabaseError


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

    async def find_by_email(self, email: str):
        return await self._find_one({ 'email': email })

    async def find_by_id(self, user_id: UUID):
        if not isinstance(user_id, UUID):
            raise InvalidId(user_id)

        return await self._find_one({ 'id': user_id })

    def _create_user(self, cursor):
        user = User(
            id=cursor.id,
            names=cursor.names,
            last_names=cursor.last_names,
            email=cursor.email,
            created_at=cursor.created_at,
            updated_at=cursor.updated_at
        )
        password = Password(cursor.password_hash, cursor.password_salt)
        user.add_password(password=password)

        return user

    async def _find_one(self, query: dict):
        statement = Users \
            .select()

        for key, value in query.items():
            statement = statement.where(Users.c[key] == value)

        statement = statement.limit(1)

        try:
            cursor = await self._database.execute(statement)

            return self._create_user(cursor.one())
        except NoResultFound as error:
            raise UserNotFound(query) from error
        except Exception as error:
            raise SQLDatabaseError(error)
