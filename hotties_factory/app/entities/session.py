from datetime import datetime
from uuid import UUID

from hotties_factory.app.core.entity import Entity

class Session(Entity):
    def __init__(
        self,
        user_id: UUID,
        id: UUID = None,
        expires_at: datetime = None,
        is_active: bool = False,
        token: str = None,
        created_at: datetime = None,
        updated_at: datetime = None
    ):
        super().__init__(id, created_at, updated_at)

        self.user_id = user_id
        self.expires_at = expires_at
        self.is_active = is_active
        self.token = token
