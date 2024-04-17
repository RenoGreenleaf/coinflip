class World(dict):
	"""Container for objects shared among scenes."""
	def __init__(self):
		super().__init__()
		self['events'] = set()
		self['cli'] = CLI()


class CLI:
	"""Provides explicit access to a command line interface."""
	def input(self, prompt):
		return input(prompt)

	def print(self, text):
		print(text)