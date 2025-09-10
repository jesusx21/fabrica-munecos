from asyncio import AbstractEventLoop, new_event_loop, set_event_loop
from uuid import uuid4

from unittest import TestCase as FalconTestCase

from tests.config import TestConfig

from hotties_factory.database.stores.memory import InMemoryDatabase

class TestCase(FalconTestCase):
    _loop: AbstractEventLoop

    def setUp(self):
        super().setUp()

        self._start_event_loop()
        self.set_up()
        self._database = None

    def set_up(self):
        pass

    def tearDown(self):
        super().tearDown()

        self._stop_event_loop()
        self.tear_down()

    def tear_down(self):
        pass
    
    def generate_uuid(self):
        return uuid4()

    def get_config(self):
        config = TestConfig('./config.ini')

        config.use_in_memory_database()

        return config

    def get_database(self):
        print()
        if not getattr(self, '_database', None):
            self._database = InMemoryDatabase()

        print(self._database.users)
        return self._database

    def wait_for(self, task):
        if not self._is_loop_running():
            self._start_event_loop()

        return self._loop.run_until_complete(task)

    def _is_loop_running(self) -> bool:
        try:
            return self._loop.is_running()
        except AttributeError:
            return False

    def _start_event_loop(self):
        if self._is_loop_running():
            return self._loop

        self._loop = new_event_loop()

        set_event_loop(self._loop)

    def _stop_event_loop(self):
        if self._is_loop_running():
            self._loop.close()
