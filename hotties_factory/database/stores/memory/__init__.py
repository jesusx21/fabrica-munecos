from hotties_factory.database.stores.memory.profiles import InMemoryProfilesStore
from hotties_factory.database.stores.memory.users import InMemoryUsersStore


class InMemoryDatabase:
    def __init__(self):
        self._initialize_stores()

    def _initialize_stores(self):
        self.profiles = InMemoryProfilesStore()
        self.users = InMemoryUsersStore()
