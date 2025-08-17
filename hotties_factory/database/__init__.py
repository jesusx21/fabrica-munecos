from sqlalchemy.ext.asyncio import create_async_engine

from .errors import DatabaseDriverNotSupported
from .stores.memory import InMemoryDatabase
from .stores.sql import SQLDatabase
from hotties_factory.config import Config

SQL_DRIVER = 'sql'
MEMORY_DRIVER = 'memory'


class DatabaseFactory:
    def __init__(self, config: Config):
        self._config = config

    def get_database(self):
        driver = self._config.get_database_driver()

        if driver == SQL_DRIVER:
            engine = self._create_sql_engine()
            return SQLDatabase(engine)
        elif driver == MEMORY_DRIVER:
            return InMemoryDatabase()
        else:
            raise DatabaseDriverNotSupported(driver)

    def _create_sql_engine(self):
        return create_async_engine(self._config.get_sql_database_connection_url())
