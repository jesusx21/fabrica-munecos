from assertpy import assert_that

from tests.test_case import TestCase

from hotties_factory.database import DatabaseFactory
from hotties_factory.database.errors import DatabaseDriverNotSupported
from hotties_factory.database.stores.memory import InMemoryDatabase
from hotties_factory.database.stores.sql import SQLDatabase

class TestDatabaseFactory(TestCase):
    def set_up(self):
        self.config = self.get_config()

    def test_get_database_with_driver_sql(self):
        self.config.use_sql_database()

        database_factory = DatabaseFactory(self.config)
        database = database_factory.get_database()

        assert_that(database).is_instance_of(SQLDatabase)

    def test_get_database_with_driver_memory(self):
        self.config.use_in_memory_database()

        database_factory = DatabaseFactory(self.config)
        database = database_factory.get_database()

        assert_that(database).is_instance_of(InMemoryDatabase)

    def test_get_database_with_invalid_driver(self):
        self.config.database_driver = 'invalid'

        database_factory = DatabaseFactory(self.config)

        assert_that(
            database_factory.get_database
        ).raises(DatabaseDriverNotSupported)
