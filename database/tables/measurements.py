from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import Column, ForeignKey, Table
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.functions import now
from sqlalchemy.types import DateTime, Float, Integer

from database.metadata import metadata

Measurements = Table(
    'measurements',
    metadata,
    Column('id', UUID, primary_key=True, server_default=text('gen_random_uuid()')),
    Column('profile_id', UUID, ForeignKey('profiles.id'), nullable=False),
    Column('height', Float, nullable=False),
    Column('weight', Float, nullable=False),
    Column('bmi', Float, nullable=False),
    Column('fat_percentage', Float, nullable=False),
    Column('body_fat_weight', Float, nullable=False),
    Column('skeletal_muscle_mass_percentage', Float, nullable=False),
    Column('skeletal_muscle_weight', Float, nullable=False),
    Column('muscle_percentage', Float, nullable=False),
    Column('muscle_weight', Float, nullable=False),
    Column('water_percentage', Float, nullable=False),
    Column('water_weight', Float, nullable=False),
    Column('visceral_fat', Float, nullable=False),
    Column('bone_mass', Float, nullable=False),
    Column('metabolism', Float, nullable=False),
    Column('protein_percentage', Float, nullable=False),
    Column('obesity_degree_percentage', Float, nullable=False),
    Column('body_age', Integer, nullable=False),
    Column('weight_without_fat', Float, nullable=False),
    Column('date', DateTime, server_default=now(), nullable=False),
    Column('created_at', DateTime, server_default=now(), nullable=False)
)
