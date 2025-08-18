from hotties_factory.database.stores.errors import NotFound, UserNotFound
from hotties_factory.database.stores.memory.store import InMemoryStore


class InMemoryUsersStore(InMemoryStore):
    def __init__(self):
        super().__init__('User')

    async def find_by_email(self, email):
        try:
            return await self._find_one({ 'email', email })
        except NotFound:
            raise UserNotFound({ 'email', email })

    async def find_by_id(self, user_id):
        try:
            return await super().find_by_id(user_id)
        except NotFound:
            raise UserNotFound({ 'id': user_id })
