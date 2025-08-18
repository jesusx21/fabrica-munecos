from uuid import UUID

from sqlalchemy.exc import IntegrityError, NoResultFound

from database.tables import Sessions
from hotties_factory.app.entities import Session
from hotties_factory.database.stores.errors import InvalidId, SessionNotFound, UserNotFound
from hotties_factory.database.stores.sql.errors import SQLDatabaseError


class SQLSessionsStore:
    def __init__(self, database):
        self._database = database

    async def create(self, session: Session):
        statement = Sessions \
            .insert() \
            .values(
                expires_at=session.expires_at,
                is_active=session.is_active,
                token=session.token,
                user_id=session.user_id
            )

        try:
            cursor = await self._database.execute(statement)
        except IntegrityError as error:
            raise UserNotFound({ 'id': session.user_id }) from error
        except Exception as error:
            raise SQLDatabaseError(error)

        session_id = cursor.inserted_primary_key[0]

        return await self.find_by_id(session_id)

    async def find_by_id(self, session_id: UUID):
        if not isinstance(session_id, UUID):
            raise InvalidId(session_id)

        return await self._find_one({ 'id': session_id })

    async def find_by_token(self, token: str):
        return await self._find_one({ 'token': token })

    def _create_session(self, cursor):
        session = Session(
            id=cursor.id,
            expires_at=cursor.expires_at,
            is_active=cursor.is_active,
            token=cursor.token,
            user_id=cursor.user_id,
            created_at=cursor.created_at,
            updated_at=cursor.updated_at
        )

        return session

    async def _find_one(self, query: dict):
        statement = Sessions \
            .select()

        for key, value in query.items():
            statement = statement.where(Sessions.c[key] == value)

        statement = statement.limit(1)

        try:
            cursor = await self._database.execute(statement)

            return self._create_session(cursor.one())
        except NoResultFound as error:
            raise SessionNotFound(query) from error
        except Exception as error:
            raise SQLDatabaseError(error)
