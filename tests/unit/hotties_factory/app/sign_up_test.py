from unittest.mock import patch
from assertpy import assert_that

from tests.test_case import TestCase

from hotties_factory.app.errors import EmailAlreadyRegistered, CouldNotRegisteredUser
from hotties_factory.database.errors import DatabaseError
from hotties_factory.app.sign_up import SignUp
from hotties_factory.app.entities import Session, User

class TestSignUpUser(TestCase):
    def set_up(self):
        self.database = self.get_database()
        self.sign_up = SignUp(
            self.database,
            'jon@gmail.com',
            'password',
            'Jon',
            'Doe'
        )

    def test_returns_session(self):
        session = self.wait_for(self.sign_up.execute())

        assert_that(session).is_instance_of(Session)
        assert_that(session.id).is_not_none()
        assert_that(session.is_active).is_true()
        assert_that(session.user_id).is_not_none()

    def test_creates_user(self):
        session = self.wait_for(self.sign_up.execute())
        user = self.wait_for(self.database.users.find_by_id(session.user_id))

        assert_that(user).is_instance_of(User)
        assert_that(user.names).is_equal_to('Jon')
        assert_that(user.last_names).is_equal_to('Doe')
        assert_that(user.email).is_equal_to('jon@gmail.com')
        assert_that(user.password).is_not_equal_to('password')
        assert_that(user.password.salt).is_not_none()
        assert_that(user.password.hash).is_not_none()
        assert_that(user.does_password_match('password')).is_true()

    def test_creates_user_with_email_already_used(self):
        self.wait_for(self.sign_up.execute())

        assert_that(self.wait_for) \
            .raises(EmailAlreadyRegistered) \
            .when_called_with(self.sign_up.execute())

    def test_create_user_fails(self):
        with patch.object(self.sign_up._database.users, 'create') as mock:
            mock.side_effect = DatabaseError()

            assert_that(self.wait_for) \
                .raises(CouldNotRegisteredUser) \
                .when_called_with(self.sign_up.execute())
