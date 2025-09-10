from hotties_factory.app.entities import User
from hotties_factory.database.stores.errors import EmailAlreadyUsed, NotFound, UserNotFound
from hotties_factory.database.stores.memory.store import InMemoryStore


class InMemoryUsersStore(InMemoryStore[User]):
    def __init__(self):
        super().__init__('User')

    async def create(self, user):
        existent_user: User = None

        try:
            existent_user = await self.find_by_email(user.email)
        except UserNotFound:
            pass

        if existent_user is not None:
            raise EmailAlreadyUsed(user.email)

        return await super().create(user)

    async def find_by_email(self, email) -> User:
        try:
            return await self._find_one({ 'email': email })
        except NotFound:
            raise UserNotFound({ 'email': email })

    async def find_by_id(self, user_id) -> User:
        try:
            return await super().find_by_id(user_id)
        except NotFound:
            raise UserNotFound({ 'id': user_id })
