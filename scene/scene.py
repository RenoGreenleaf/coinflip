class Scene:
	"""Commonly available commands."""
	def __init__(self, cli, events):
		self.slug = ''
		self.cli = cli
		self.events = events

	def request(self):
		"""Asks what to do next."""
		self.cli.print("Enter a command")

	def execute(self, command):
		if command == 'help':
			self.events['scene.asked_for_help'].trigger()
			self.cli.print("Help was requested.")
		elif command == 'exit':
			self.events['scene.decided_to_exit'].trigger()
		elif command == 'menu':
			self.events['scene.asked_for_menu'].trigger()
		else:
			self.cli.print("Unclear.\n")

	def editable_execute(self, command):
		self.cli.print("There's nothing to edit in the scene.")

	def prompt(self):
		"""Prefixes users input."""
		return '> '

	def play(self):
		self.request()
		command = self.cli.input(self.prompt())
		self.execute(command)

	def start_listening(self):
		pass

	def notify(self, event):
		pass

	def load(self, scene_data, events):
		self.slug = scene_data.get('slug', '')

	def serialize(self):
		return {}

	def __repr__(self):
		return self.slug
