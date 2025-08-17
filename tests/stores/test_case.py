import os

from sqlalchemy.ext.asyncio import create_async_engine

from unittest import IsolatedAsyncioTestCase
from tests.config import TestConfig

from database import metadata
from hotties_factory.database.stores.sql import SQLDatabase


class DatabaseTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self._engine = self.create_engine()

        async with self._engine.begin() as connection:
            await connection.run_sync(metadata.create_all)

    async def asyncTearDown(self):
        async with self._engine.begin() as connection:
            await connection.run_sync(metadata.drop_all)

        await self._engine.dispose()

    async def execute(self, statement):
        async with self._engine.begin() as connection:
            return await connection.execute(statement)

    def create_engine(self):
        config = self.get_config()

        return create_async_engine(config.get_sql_database_connection_url())

    def get_config(self):
        return TestConfig(self.get_config_path())

    def get_config_path(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        return os.path.normpath(os.path.join(dir_path, '../../', 'config.ini'))

    def get_database(self):
        return SQLDatabase(self._engine)
