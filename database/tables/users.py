from sqlalchemy.schema import Column, Table
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.functions import now
from sqlalchemy.types import DateTime, String

from database.metadata import metadata
from database.types import GUID

Users = Table(
    'users',
    metadata,
    Column('id', GUID, primary_key=True, server_default=text('gen_random_uuid()')),
    Column('names', String(250), nullable=False),
    Column('last_names', String(250), nullable=False),
    Column('email', String(150), nullable=False, unique=True),
    Column('password_hash', String(200), nullable=False),
    Column('password_salt', String(200), nullable=False),
    Column('created_at', DateTime, server_default=now(), nullable=False),
    Column('updated_at', DateTime, server_default=now(), onupdate=now(), nullable=False)
)
