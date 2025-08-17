from unittest import TestCase as FalconTestCase

from .config import TestConfig

class TestCase(FalconTestCase):
    def setUp(self):
        super().setUp()

        self.set_up()

    def set_up(self):
        pass

    def tearDown(self):
        super().tearDown()

        self.tear_down()

    def tear_down(self):
        pass

    def get_config(self):
        config = TestConfig('./config.ini')

        config.use_in_memory_database()

        return config
