def default_action(events, cli):
	cli.print("Wha-a-a-a-at?\n")


def default_condition(events):
	return True


class Option:
	def __init__(
		self,
		description,
		action=default_action,
		condition=default_condition
	):
		self.description = description
		self.select = action
		self.is_available = condition

	def describe(self):
		return self.description
