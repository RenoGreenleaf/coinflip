from scene import scene


class Conversation(scene.Scene):
	def __init__(self, cli, events, options):
		super().__init__(cli, events)
		self.options = options
		self.back_chosen = events['scene.asked_for_menu']

	def request(self):
		item = 0
		self.available_options = []

		for option in self.options:
			self._add_option(option)

		for option in self.available_options:
			item += 1
			self.cli.print(f'{item}. {option.describe()}')

	def execute(self, command):
		if not command.isnumeric():
			return super().execute(command)

		option = self.available_options[int(command) - 1]
		option.select(self.cli)

	def prompt(self):
		return f'[1-{len(self.available_options)}]> '

	def _add_option(self, option):
		if option.is_available():
			self.available_options.append(option)

	def start_listening(self):
		for option in self.options:
			option.start_listening()

	def notify(self, event):
		pass
