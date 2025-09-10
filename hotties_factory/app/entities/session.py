from datetime import datetime, timezone
from uuid import UUID

from dateutil.relativedelta import relativedelta
from Crypto.Random import get_random_bytes

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
        self._session_token = token
        
    @property
    def token(self):
        return self._session_token

    def activate_token(self):
        if self.is_active:
            return self

        today = datetime.now(timezone.utc).date()
        delta = relativedelta(year=1)
        self.expires_at = today + delta
        self.is_active = True

        return self

    def deactivate_token(self):
        if not self.is_expired():
            self.expires_at = datetime.now()

        self.is_active = False

        return self

    def generate_token(self):
        self.deactivate_token()
        self._session_token = get_random_bytes(32).hex()

        return self

    def is_expired(self) -> bool:
        if self.expires_at is None:
            return True

        return self.expires_at <= datetime.now()
