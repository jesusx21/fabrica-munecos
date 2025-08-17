from datetime import date
from uuid import uuid4

from tests.stores.sql.fixtures import constants

profiles_data = [
    {
        'id': uuid4(),
        'name': 'Juanito',
        'birthdate': date(1990, 5, 12),
        'height': 1_75,
        'weight': 78_50,
        'user_id': None
    },
    {
        'id': constants.WITH_USER_PROFILE_ID,
        'name': 'Mary',
        'birthdate': date(1988, 9, 23),
        'height': 1_62,
        'weight': 60_00,
        'user_id': constants.USER_ID
    },
    {
        'id': constants.WITHOUT_USER_PROFILE_ID,
        'name': 'Luisito',
        'birthdate': date(1995, 1, 8),
        'height': 1_80,
        'weight': 85_30,
        'user_id': None
    },
    {
        'id': uuid4(),
        'name': 'Ana',
        'birthdate': date(1992, 3, 15),
        'height': 1_67,
        'weight': 58_70,
        'user_id': None
    },
    {
        'id': uuid4(),
        'name': 'Carlos',
        'birthdate': date(1985, 11, 30),
        'height': 1_72,
        'weight': 74_20,
        'user_id': None
    }
]
