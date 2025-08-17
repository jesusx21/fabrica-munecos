from uuid import UUID

from sqlalchemy.exc import IntegrityError, NoResultFound

from database.tables import Profiles
from hotties_factory.app.entities import Profile
from hotties_factory.database.stores.errors import InvalidId, ProfileNotFound, UserNotFound
from hotties_factory.database.stores.sql.errors import SQLDatabaseError


class SQLProfilesStore:
    def __init__(self, database):
        self._database = database

    async def create(self, profile: Profile):
        statement = Profiles \
            .insert() \
            .values(
                name=profile.name,
                birthdate=profile.birthdate,
                height=profile.height,
                weight=profile.weight,
                user_id=profile.user_id
            )

        try:
            cursor = await self._database.execute(statement)
        except IntegrityError as error:
            raise UserNotFound({ 'id': profile.user_id }) from error
        except Exception as error:
            raise SQLDatabaseError(error)

        profile_id = cursor.inserted_primary_key[0]

        return await self.find_by_id(profile_id)

    async def find_by_id(self, profile_id: UUID):
        if not isinstance(profile_id, UUID):
            raise InvalidId(profile_id)

        statement = Profiles \
            .select() \
            .where(Profiles.c.id == profile_id)

        try:
            cursor = await self._database.execute(statement)

            return self._create_profile(cursor.one())
        except NoResultFound as error:
            raise ProfileNotFound({ 'id': profile_id }) from error
        except Exception as error:
            raise SQLDatabaseError(error)

    def _create_profile(self, cursor):
        profile = Profile(
            id=cursor.id,
            name=cursor.name,
            birthdate=cursor.birthdate,
            height=cursor.height,
            weight=cursor.weight,
            user_id=cursor.user_id,
            created_at=cursor.created_at,
            updated_at=cursor.updated_at
        )

        return profile
