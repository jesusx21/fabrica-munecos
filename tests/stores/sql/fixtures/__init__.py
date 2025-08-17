from .users import users_data


class Fixtures:
	def __init__(self):
		self.users = users_data


fixtures = Fixtures()
