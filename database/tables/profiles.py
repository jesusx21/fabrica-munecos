from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import Column, ForeignKey, Table
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.functions import now
from sqlalchemy.types import Date, DateTime, Integer, String

from database.metadata import metadata

Profiles = Table(
    'profiles',
    metadata,
    Column('id', UUID, primary_key=True, server_default=text('gen_random_uuid()')),
    Column('name', String(256), nullable=False),
    Column('birthdate', Date),
    Column('height', Integer, nullable=False),
    Column('weight', Integer, nullable=False),
    Column('user_id', UUID, ForeignKey('users.id'), nullable=True, unique=True),
    Column('created_at', DateTime, server_default=now(), nullable=False),
    Column('updated_at', DateTime, server_default=now(), onupdate=now(), nullable=False)
)
