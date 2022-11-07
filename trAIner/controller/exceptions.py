


class UserIndexError(Exception):
	def __str__(self):
		return "User Index 범위를 초과함."


class ItemIndexError(Exception):
	def __str__(self):
		return "Item(Problem) Index 범위를 초과함."
