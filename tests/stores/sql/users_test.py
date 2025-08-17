from datetime import datetime
from unittest.mock import patch
from uuid import UUID, uuid4

from assertpy import assert_that

from ..test_case import DatabaseTestCase
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

        assert_that(user_created.id).is_instance_of(UUID)
        assert_that(user_created.names).is_equal_to('Jon')
        assert_that(user_created.last_names).is_equal_to('Doe')
        assert_that(user_created.email).is_equal_to('jon.doe@gmail.com')
        assert_that(user_created.password).is_instance_of(Password)
        assert_that(user_created.password.hash).is_equal_to('fake-hash')
        assert_that(user_created.password.salt).is_equal_to('fake-salt')
        assert_that(user_created.created_at).is_equal_to_ignoring_milliseconds(datetime.now())
        assert_that(user_created.updated_at).is_equal_to_ignoring_milliseconds(datetime.now())

    async def test_create_with_repeated_email(self):
        self.user.email = 'luis.hernandez@example.com'

        with self.assertRaises(EmailAlreadyUsed):
            await self.database.users.create(self.user)

    async def test_create_user_when_database_fails(self):
        with patch.object(self.database, 'execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(SQLDatabaseError):
                await self.database.users.create(self.user)


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
