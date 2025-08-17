from uuid import uuid4

from . import constants

users_data = [
    {
        'id': uuid4(),
        'names': 'Juan Carlos',
        'last_names': 'Ramírez López',
        'email': 'juan.ramirez@example.com',
        'password_hash': 'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3',
        'password_salt': 'random_salt_123'
    },
    {
        'id': constants.USER_ID,
        'names': 'María Fernanda',
        'last_names': 'González Pérez',
        'email': 'maria.gonzalez@example.com',
        'password_hash': '5f4dcc3b5aa765d61d8327deb882cf99',
        'password_salt': 'salt_maria_456'
    },
    {
        'id': uuid4(),
        'names': 'Luis Alberto',
        'last_names': 'Hernández Díaz',
        'email': 'luis.hernandez@example.com',
        'password_hash': '2c1743a391305fbf367df8e4f069f9f9',
        'password_salt': 'salt_luis_789'
    },
    {
        'id': uuid4(),
        'names': 'Ana Sofía',
        'last_names': 'Martínez Torres',
        'email': 'ana.martinez@example.com',
        'password_hash': '098f6bcd4621d373cade4e832627b4f6',
        'password_salt': 'sofia_salt_101'
    },
    {
        'id': uuid4(),
        'names': 'Carlos Eduardo',
        'last_names': 'Flores Mendoza',
        'email': 'carlos.flores@example.com',
        'password_hash': '202cb962ac59075b964b07152d234b70',
        'password_salt': 'carlos_salt_202'
    }
]
