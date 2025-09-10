from hotties_factory.database import Database
from hotties_factory.app.entities import Session, User
from hotties_factory.database.stores.errors import EmailAlreadyUsed
from hotties_factory.app.errors import CouldNotRegisteredUser, EmailAlreadyRegistered


class SignUp():
    def __init__(
        self,
        database: Database,
        email: str,
        password: str,
        names: str,
        last_names: str
    ):
        self._database = database
        self._email = email
        self._raw_passsword = password
        self._names = names
        self._last_names = last_names

    async def execute(self):
        user = await self._create_user()
        session = await self._create_session(user)

        return session

    async def _create_session(self, user: User):
        session = Session(user_id=user.id)


        session.generate_token() \
            .activate_token()
        try:
            return await self._database \
                .sessions \
                .create(session)
        except Exception as error:
            raise CouldNotRegisteredUser(error)

    async def _create_user(self) -> User:
        user = User(
            names=self._names,
            last_names=self._last_names,
            email=self._email
        )

        user.add_password(raw_password=self._raw_passsword)

        try:
            user = await self._database.users.create(user)
        except EmailAlreadyUsed:
            raise EmailAlreadyRegistered(self._email)
        except Exception as error:
            raise CouldNotRegisteredUser(error)

        return user
