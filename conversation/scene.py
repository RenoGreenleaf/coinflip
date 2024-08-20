from scene import scene


class Conversation(scene.Scene):
	def __init__(self, cli, events, options, slug):
		super().__init__(cli, events)
		self.options = options
		self.slug = slug
		self.back_chosen = events['scene.asked_for_menu']

	def request(self):
		item = 0
		self.available_options = []

		for option in self.options:
			self._add_option(option)

		for option in self.available_options:
			item += 1
			self.cli.print(f'{item}. {option.describe()}')

		self.cli.print(f'{item+1}. Back.')

	def execute(self, command):
		if not command.isnumeric():
			return super().execute(command)

		if int(command) == len(self.available_options) + 1:  # "back" option is chosen.
			self.back_chosen.trigger()

		option = self.available_options[int(command) - 1]
		next_scene_slug = option.select(self.events, self.cli)

		if next_scene_slug:
			return next_scene_slug

		return self.slug

	def prompt(self):
		return f'[1-{len(self.available_options)+1}]> '

	def _add_option(self, option):
		if option.is_available(self.events):
			self.available_options.append(option)