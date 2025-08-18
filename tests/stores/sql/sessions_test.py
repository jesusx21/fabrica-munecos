from datetime import datetime, timedelta
from unittest.mock import patch
from uuid import UUID, uuid4

from tests.stores.sql.fixtures import constants, fixtures
from tests.stores.test_case import DatabaseTestCase

from database.tables import Sessions, Users
from hotties_factory.app.entities import Session
from hotties_factory.database.stores.errors import InvalidId, SessionNotFound, UserNotFound
from hotties_factory.database.stores.sql.errors import SQLDatabaseError


class TestSQLSessionsStore(DatabaseTestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        await self._create_users()
        await self._create_sessions()

        self.database = self.get_database()

    async def _create_sessions(self):
        statement = Sessions \
            .insert() \
            .values(fixtures.sessions)

        await self.execute(statement)

    async def _create_users(self):
        statement = Users \
            .insert() \
            .values(fixtures.users)

        await self.execute(statement)


class TestCreateSession(TestSQLSessionsStore):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.session = Session(
            token='thisIsAToken',
            user_id=constants.USER_ID,
            expires_at=datetime.now() + timedelta(days=7),
            is_active=True
        )

    async def test_create_session(self):
        session_created = await self.database.sessions.create(self.session)

        self.assertIsInstance(session_created.id, UUID)
        self.assertEqual(session_created.token, 'thisIsAToken')
        self.assertEqual(session_created.user_id, constants.USER_ID)
        self.assertEqual(session_created.expires_at, self.session.expires_at)
        self.assertTrue(session_created.is_active)
        self.assertIsInstance(session_created.created_at, datetime)
        self.assertIsInstance(session_created.updated_at, datetime)

    async def test_create_session_with_not_existent_user(self):
        self.session.user_id = uuid4()

        with self.assertRaises(UserNotFound):
            await self.database.sessions.create(self.session)

    async def test_create_session_when_database_fails(self):
        with patch.object(self.database, 'execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(SQLDatabaseError):
                await self.database.sessions.create(self.session)


class TestFindSessionsById(TestSQLSessionsStore):
    async def test_find_session_by_id(self):
        session = await self.database.sessions.find_by_id(constants.ACTIVE_FOR_USER_SESSION_ID)

        self.assertEqual(session.id, constants.ACTIVE_FOR_USER_SESSION_ID)
        self.assertEqual(session.token, 'token_mary_789xyz')
        self.assertTrue(session.is_active)

        self.assertIsInstance(session, Session)
        self.assertIsInstance(session.created_at, datetime)
        self.assertIsInstance(session.updated_at, datetime)

    async def test_find_session_with_invalid_id(self):
        with self.assertRaises(InvalidId):
            await self.database.sessions.find_by_id(str(uuid4()))

    async def test_find_session_with_not_existent_id(self):
        with self.assertRaises(SessionNotFound):
            await self.database.sessions.find_by_id(uuid4())

    async def test_find_session_when_database_fails(self):
        with patch.object(self.database, 'execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(SQLDatabaseError):
                await self.database.sessions.find_by_id(constants.ACTIVE_FOR_FIRST_USER_SESSION_ID)
