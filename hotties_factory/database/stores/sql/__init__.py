from sqlalchemy.ext.asyncio import AsyncEngine

from hotties_factory.database.stores.sql.profiles import SQLProfilesStore
from hotties_factory.database.stores.sql.sessions import SQLSessionsStore
from hotties_factory.database.stores.sql.users import SQLUsersStore


class SQLDatabase:
    def __init__(self, engine: AsyncEngine):
        self._engine = engine

        self._initialize_stores()

    async def execute(self, statement):
        async with self._engine.begin() as connection:
            return await connection.execute(statement)

    def _initialize_stores(self):
        self.profiles = SQLProfilesStore(self)
        self.sessions = SQLSessionsStore(self)
        self.users = SQLUsersStore(self)
