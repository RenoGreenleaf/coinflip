class Scene:
	"""Commonly available commands."""
	def __init__(self, cli, events):
		self.slug = ''
		self.cli = cli
		self.events = events

	def request(self):
		"""Asks what to do next."""
		print("Enter a command")

	def execute(self, command):
		if command == 'help':
			return 'help'
		elif command == 'exit':
			return 'exit'
		elif command == 'menu':
			return 'menu'
		else:
			print("Unclear.\n")
			return self.slug

	def prompt(self):
		"""Prefixes users input."""
		return '> '

	def play(self):
		self.request()
		command = self.cli.input(self.prompt())
		return self.execute(command)
