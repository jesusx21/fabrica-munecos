from ..errors import NotFound, UserNotFound
from .store import InMemoryStore


class InMemoryUsersStore(InMemoryStore):
    def __init__(self):
        super().__init__('User')

    async def find_by_id(self, job_id):
        try:
            return await super().find_by_id(job_id)
        except NotFound:
            raise UserNotFound({ 'id': job_id })
