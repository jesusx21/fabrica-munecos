from datetime import datetime, timedelta

from tests.stores.sql.fixtures import constants

sessions_data = [
    {
        'id': constants.ACTIVE_FOR_FIRST_USER_SESSION_ID,
        'token': 'token_juan_123456',
        'user_id': constants.FIRST_USER_ID,
        'expires_at': datetime.now() + timedelta(days=7),
        'is_active': True
    },
    {
        'id': constants.INACTIVE_FOR_FIRST_USER_SESSION_ID,
        'token': 'token_carlos_abcdef',
        'user_id': constants.FIRST_USER_ID,
        'expires_at': datetime.now() - timedelta(days=7),
        'is_active': False
    },
    {
        'id': constants.ACTIVE_FOR_USER_SESSION_ID,
        'token': 'token_mary_789xyz',
        'user_id': constants.USER_ID,
        'expires_at': datetime.now() + timedelta(days=7),
        'is_active': True
    },
    {
        'id': constants.INACTIVE_FOR_USER_SESSION_ID,
        'token': 'token_fer_456def',
        'user_id': constants.USER_ID,
        'expires_at': datetime.now() - timedelta(days=7),
        'is_active': False
    }
]
