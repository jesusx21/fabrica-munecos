from hotties_factory.app.entities import Session

from hotties_factory.database.stores.errors import NotFound, SessionNotFound
from hotties_factory.database.stores.memory.store import InMemoryStore


class InMemorySessionsStore(InMemoryStore[Session]):
    def __init__(self):
        super().__init__('Session')

    async def find_by_id(self, session_id) -> Session:
        try:
            return await super().find_by_id(session_id)
        except NotFound:
            raise SessionNotFound({ 'id': session_id })

    async def find_by_token(self, token) -> Session:
        try:
            return await self._find_one({ 'token', token })
        except NotFound:
            raise SessionNotFound({ 'token', token })
