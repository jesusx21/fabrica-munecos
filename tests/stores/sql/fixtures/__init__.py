from tests.stores.sql.fixtures.profiles import profiles_data
from tests.stores.sql.fixtures.users import users_data


class Fixtures:
	def __init__(self):
		self.profiles = profiles_data
		self.users = users_data


fixtures = Fixtures()
