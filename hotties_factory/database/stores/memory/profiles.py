from hotties_factory.database.stores.errors import NotFound, ProfileNotFound
from hotties_factory.database.stores.memory.store import InMemoryStore


class InMemoryProfilesStore(InMemoryStore):
    def __init__(self):
        super().__init__('Profile')

    async def find_by_id(self, profile_id):
        try:
            return await super().find_by_id(profile_id)
        except NotFound:
            raise ProfileNotFound({ 'id': profile_id })
