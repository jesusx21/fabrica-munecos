from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import Column, ForeignKey, Table
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.functions import now
from sqlalchemy.types import Boolean, DateTime, String

from database.metadata import metadata

Sessions = Table(
    'sessions',
    metadata,
    Column('id', UUID, primary_key=True, server_default=text('gen_random_uuid()')),
    Column('token', String(500), nullable=False, unique=True),
    Column('user_id', UUID, ForeignKey('users.id'), nullable=False),
    Column('expires_at', DateTime, nullable=False),
    Column('is_active', Boolean(), default=False),
    Column('created_at', DateTime, server_default=now(), nullable=False),
    Column('updated_at', DateTime, server_default=now(), onupdate=now(), nullable=False)
)
