
from sqlalchemy.ext.asyncio import AsyncEngine


class SQLDatabase:
    def __init__(self, engine: AsyncEngine):
        self._engine = engine

        self._initialize_stores()

    async def execute(self, statement):
        async with self._engine.begin() as connection:
            return await connection.execute(statement)

    def _initialize_stores(self):
        pass
