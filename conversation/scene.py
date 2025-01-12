from scene import scene
from conversation.option import Option


class Conversation(scene.Scene):
	def __init__(self, cli, events, options):
		super().__init__(cli, events)
		self.options = []

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

	def editable_execute(self, command):
		if command == 'list':
			self._list()
		else:
			self.cli.print("Unclear.")

	def prompt(self):
		return f'[1-{len(self.available_options)}]> '

	def start_listening(self):
		for option in self.options:
			option.start_listening()

	def notify(self, event):
		pass

	def load(self, scene_data, events):
		super().load(scene_data, events)

		for option_data in scene_data['options']:
			self._load_option(option_data, events)

	def serialize(self):
		return {
			'type': 'conversation'
		}

	def list(self):
		offset = 0
		result = []

		for option in self.options:
			offset += 1
			result.append(f"{offset}. {option}")

		return result

	def _add_option(self, option):
		if option.is_available():
			self.available_options.append(option)

	def _load_option(self, option_data, events):
		self.options.append(Option(
			description=option_data['description'],
			triggers=events[option_data.get('triggers', 'none')],
			hide_condition=events[option_data.get('hide_condition', 'none')],
			show_condition=events[option_data.get('show_condition', 'none')],
			available=option_data.get('available', True),
			message=option_data.get('message', "")
		))

	def _list(self):
		self.cli.print("Options:")
		offset = 0

		for option in self.options:
			offset += 1
			self.cli.print(f"\t{offset}.", option)
