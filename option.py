def default_action():
	print("Wha-a-a-a-at?\n")


class Option:
	def __init__(self, description, action=default_action):
		self.description = description
		self.select = action

	def describe(self):
		return self.description
