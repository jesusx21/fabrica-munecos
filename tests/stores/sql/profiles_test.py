from datetime import date, datetime
from unittest.mock import patch
from uuid import UUID, uuid4

from tests.stores.sql.fixtures import constants, fixtures
from tests.stores.test_case import DatabaseTestCase

from database.tables import Profiles, Users
from hotties_factory.app.entities import Profile
from hotties_factory.database.stores.errors import InvalidId, ProfileNotFound, UserNotFound
from hotties_factory.database.stores.sql.errors import SQLDatabaseError


class TestSQLProfilesStore(DatabaseTestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        await self._create_users()
        await self._create_profiles()

        self.database = self.get_database()

    async def _create_profiles(self):
        statement = Profiles \
            .insert() \
            .values(fixtures.profiles)

        await self.execute(statement)

    async def _create_users(self):
        statement = Users \
            .insert() \
            .values(fixtures.users)

        await self.execute(statement)


class TestCreateProfile(TestSQLProfilesStore):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.profile = Profile(
            name='Jhonny',
            birthdate=date(1990, 2, 14),
            height=1_80,
            weight=90_00
        )

    async def test_create_profile_with_user(self):
        self.profile.user_id = constants.FIRST_USER_ID

        profile_created = await self.database.profiles.create(self.profile)

        self.assertIsInstance(profile_created.id, UUID)
        self.assertEqual(profile_created.name, 'Jhonny')
        self.assertEqual(profile_created.birthdate, self.profile.birthdate)
        self.assertEqual(profile_created.height, 1_80)
        self.assertEqual(profile_created.weight, 90_00)
        self.assertEqual(profile_created.user_id, constants.FIRST_USER_ID)
        self.assertIsInstance(profile_created.created_at, datetime)
        self.assertIsInstance(profile_created.updated_at, datetime)

    async def test_create_profile_without_user(self):
        profile_created = await self.database.profiles.create(self.profile)

        self.assertIsInstance(profile_created.id, UUID)
        self.assertEqual(profile_created.name, 'Jhonny')
        self.assertEqual(profile_created.birthdate, self.profile.birthdate)
        self.assertEqual(profile_created.height, 1_80)
        self.assertEqual(profile_created.weight, 90_00)
        self.assertIsNone(profile_created.user_id)
        self.assertIsInstance(profile_created.created_at, datetime)
        self.assertIsInstance(profile_created.updated_at, datetime)

    async def test_create_profile_with_not_existent_user(self):
        self.profile.user_id = uuid4()

        with self.assertRaises(UserNotFound):
            await self.database.profiles.create(self.profile)

    async def test_create_user_when_database_fails(self):
        with patch.object(self.database, 'execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(SQLDatabaseError):
                await self.database.profiles.create(self.profile)


class TestFindProfilesById(TestSQLProfilesStore):
    async def test_find_profile_by_id(self):
        profile = await self.database.profiles.find_by_id(constants.WITH_USER_PROFILE_ID)

        self.assertEqual(profile.id, constants.WITH_USER_PROFILE_ID)
        self.assertEqual(profile.name, 'Mary')
        self.assertEqual(profile.birthdate, date(1988, 9, 23))
        self.assertEqual(profile.height, 1_62)
        self.assertEqual(profile.weight, 60_00)

        self.assertIsInstance(profile, Profile)
        self.assertIsInstance(profile.created_at, datetime)
        self.assertIsInstance(profile.updated_at, datetime)

    async def test_find_profile_with_invalid_id(self):
        with self.assertRaises(InvalidId):
            await self.database.profiles.find_by_id(str(uuid4()))

    async def test_find_profile_with_not_existent_id(self):
        with self.assertRaises(ProfileNotFound):
            await self.database.profiles.find_by_id(uuid4())

    async def test_find_profile_when_database_fails(self):
        with patch.object(self.database, 'execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(SQLDatabaseError):
                await self.database.profiles.find_by_id(constants.WITH_USER_PROFILE_ID)
