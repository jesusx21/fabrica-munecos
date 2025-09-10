from datetime import datetime

from tests.test_case import TestCase

from hotties_factory.app.entities import Session


class TestSession(TestCase):
    def set_up(self):
        super().set_up()

        self.session = Session({'user_id': self.generate_uuid()})


class TestActivateSessionToken(TestSession):
    def test_activates_token(self):
        self.session.activate_token()

        self.assertTrue(self.session.is_active)
        self.assertIsNotNone(self.session.expires_at)

    def test_does_not_activate_token_if_already_active(self):
        self.session.is_active = True
        self.session.expires_at = datetime(2025, 10, 1)

        self.session.activate_token()

        self.assertTrue(self.session.is_active)
        self.assertEqual(datetime(2025, 10, 1), self.session.expires_at)


class TestDeactivateSessionToken(TestSession):
    def test_deactivates_token(self):
        self.session.is_active = True
        self.session.expires_at = datetime(2025, 10, 1)

        self.session.deactivate_token()

        self.assertFalse(self.session.is_active)
        self.assertIsNotNone(self.session.expires_at)

    def test_does_not_change_expiration_if_already_expired(self):
        self.session.is_active = True
        self.session.expires_at = datetime(2020, 10, 1)

        self.session.deactivate_token()

        self.assertFalse(self.session.is_active)
        self.assertEqual(datetime(2020, 10, 1), self.session.expires_at)


class TestGenerateSessionToken(TestSession):
    def test_generates_token(self):
        self.session.generate_token()

        self.assertIsNotNone(self.session.token)
        self.assertFalse(self.session.is_active)
        self.assertIsNone(self.session.expires_at)
