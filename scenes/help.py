from options import options
from scenes import scene


class Help(scene.Scene):
	def __init__(self, cli, events):
		super().__init__(cli, events)
		self.slug = 'help'
		self.available_options = []

	def request(self):
		item = 0
		self.available_options = []

		for option in options:
			self._add_option(option)

		for option in self.available_options:
			item += 1
			self.cli.print(f'{item}. {option.describe()}')

		self.cli.print(f'{item+1}. Back.')

	def execute(self, command):
		if not command.isnumeric():
			return super().execute(command)

		if int(command) == len(self.available_options) + 1:  # "back" option is chosen.
			return 'coin_flip'

		option = self.available_options[int(command) - 1]
		option.select(self.events, self.cli)
		return self.slug

	def prompt(self):
		return f'[1-{len(self.available_options)+1}]> '

	def _add_option(self, option):
		if option.is_available(self.events):
			self.available_options.append(option)