from datetime import datetime
from unittest.mock import patch
from uuid import UUID, uuid4

from tests.stores.test_case import DatabaseTestCase
from .fixtures import constants, fixtures

from database.tables import Users
from hotties_factory.app.entities import User
from hotties_factory.app.entities.user import Password
from hotties_factory.database.stores.errors import EmailAlreadyUsed, InvalidId, UserNotFound
from hotties_factory.database.stores.sql.errors import SQLDatabaseError


class TestSQLUsersStore(DatabaseTestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        statement = Users \
            .insert() \
            .values(fixtures.users)

        await self.execute(statement)

        self.database = self.get_database()

class TestCreateUser(TestSQLUsersStore):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.user = User(
            names='Jon',
            last_names='Doe',
            email='jon.doe@gmail.com'
        )
        self.user.set_password('fake-hash', 'fake-salt')


    async def test_create_user(self):
        user_created = await self.database.users.create(self.user)

        self.assertIsInstance(user_created.id, UUID)
        self.assertEqual(user_created.names, 'Jon')
        self.assertEqual(user_created.last_names, 'Doe')
        self.assertEqual(user_created.email, 'jon.doe@gmail.com')
        self.assertIsInstance(user_created.password, Password)
        self.assertEqual(user_created.password.hash, 'fake-hash')
        self.assertEqual(user_created.password.salt, 'fake-salt')
        self.assertIsInstance(user_created.created_at, datetime)
        self.assertIsInstance(user_created.updated_at, datetime)

    async def test_create_with_repeated_email(self):
        self.user.email = 'luis.hernandez@example.com'

        with self.assertRaises(EmailAlreadyUsed):
            await self.database.users.create(self.user)

    async def test_create_user_when_database_fails(self):
        with patch.object(self.database, 'execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(SQLDatabaseError):
                await self.database.users.create(self.user)


class TestFindUserByEmail(TestSQLUsersStore):
    async def test_find_user_by_id(self):
        user = await self.database.users.find_by_email('luis.hernandez@example.com')

        self.assertIsInstance(user.id, UUID)
        self.assertEqual(user.names, 'Luis Alberto')
        self.assertEqual(user.last_names, 'Hernández Díaz')
        self.assertEqual(user.email, 'luis.hernandez@example.com')

        self.assertIsInstance(user, User)
        self.assertIsInstance(user.created_at, datetime)
        self.assertIsInstance(user.updated_at, datetime)

    async def test_find_user_with_not_existent_email(self):
        with self.assertRaises(UserNotFound):
            await self.database.users.find_by_email('not_existent@gmail.com')

    async def test_find_user_when_database_fails(self):
        with patch.object(self.database, 'execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(SQLDatabaseError):
                await self.database.users.find_by_email('luis.hernandez@example.com')


class TestFindUserById(TestSQLUsersStore):
    async def test_find_user_by_id(self):
        user = await self.database.users.find_by_id(constants.USER_ID)

        self.assertEqual(user.id, constants.USER_ID)
        self.assertEqual(user.names, 'María Fernanda')
        self.assertEqual(user.last_names, 'González Pérez')
        self.assertEqual(user.email, 'maria.gonzalez@example.com')

        self.assertIsInstance(user, User)
        self.assertIsInstance(user.created_at, datetime)
        self.assertIsInstance(user.updated_at, datetime)

    async def test_find_user_with_invalid_id(self):
        with self.assertRaises(InvalidId):
            await self.database.users.find_by_id(str(uuid4()))

    async def test_find_user_with_not_existent_id(self):
        with self.assertRaises(UserNotFound):
            await self.database.users.find_by_id(uuid4())

    async def test_find_user_when_database_fails(self):
        with patch.object(self.database, 'execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(SQLDatabaseError):
                await self.database.users.find_by_id(constants.USER_ID)
