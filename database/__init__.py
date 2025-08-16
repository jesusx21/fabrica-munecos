from sqlalchemy.ext.asyncio import create_async_engine

from hotties_factory.app.config import Config
from .stores.sql import SQLDatabase
from .errors import DatabaseDriverNotSupported

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
        else:
            raise DatabaseDriverNotSupported(driver)

    def _create_sql_engine(self):
        return create_async_engine(self._config.get_sql_database_connection_url())
