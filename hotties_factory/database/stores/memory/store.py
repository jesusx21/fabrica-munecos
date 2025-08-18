from copy import deepcopy
from datetime import datetime, timezone
from uuid import UUID, uuid4

from ..errors import InvalidId, NotFound
from hotties_factory.app.core import Entity
from hotties_factory.database.errors import DatabaseError


class InMemoryStore:
    def __init__(self, entity_name: str):
        self._entity_name = entity_name
        self._items = dict()

    async def create(self, entity: Entity):
        if not entity.id:
            entity.id = uuid4()

        if not isinstance(entity.id, UUID):
            raise InvalidId(entity.id)

        entity.created_at = datetime.now(timezone.utc)
        entity.updated_at = datetime.now(timezone.utc)

        self._items[str(entity.id)] = entity

        try:
            return deepcopy(self._items[str(entity.id)])
        except Exception as error:
            raise DatabaseError(error)

    async def find_by_id(self, entity_id):
        if not isinstance(entity_id, UUID):
            raise InvalidId(entity_id)

        try:
            return deepcopy(self._items[str(entity_id)])
        except KeyError:
            raise NotFound(self._entity_name, { 'id': entity_id })
        except Exception as error:
            raise DatabaseError(error)

    def _find_one(self, query: dict):
        try:
            for entity in self._items.values():
                if all(
                    getattr(entity, field) == value for field, value in query.items()
                ):
                    return deepcopy(entity)
        except Exception as error:
            raise DatabaseError(error)

        raise NotFound(self._entity_name, query)
