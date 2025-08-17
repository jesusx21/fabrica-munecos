from datetime import date, datetime
from uuid import UUID

from dateutil import relativedelta

from hotties_factory.app.core import Entity


class Profile(Entity):
    def __init__(
        self,
        name: str,
        birthdate: date,
        id: UUID = None,
        height: float = None,
        weight: float = None,
        user_id: UUID = None,
        created_at: datetime = None,
        updated_at: datetime = None
    ):
        super().__init__(id, created_at, updated_at)

        self.name = name
        self.birthdate = birthdate
        self.height = height
        self.weight = weight
        self.user_id = user_id

    @property
    def age(self):
        today = datetime.datetime.utcnow()
        today = today.date()

        age = relativedelta.relativedelta(today, self.birthdate)

        return age.years
