from .users import InMemoryUsersStore


class InMemoryDatabase:
    def __init__(self):
        self._initialize_stores()

    def _initialize_stores(self):
        self.users = InMemoryUsersStore()
