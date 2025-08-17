from hotties_factory.database.errors import DatabaseError


class SQLDatabaseError(DatabaseError):
    def __init__(self, error):
        super().__init__(error, 'SQL connection failed.')
