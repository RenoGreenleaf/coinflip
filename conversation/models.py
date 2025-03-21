from reusables.models import Scene
from reusables import nulls
from conversation.editor import Editor, OptionEditor
from conversation.player import Player


class Conversation(Scene):
	def __init__(self):
		self.id = 0
		self.options = []

	def wrap_for_editing(self, pool):
		return Editor(self, pool)

	def wrap_for_playing(self, pool):
		return Player(self, pool)

	def save(self):
		result = {
			'id': self.id,
			'type': 'conversation',
			'options': [],
		}

		for option in self.options:
			result['options'].append({
				'description': option.description,
				'available': option.available,
				'message': option.message,
				'triggers': option.triggers.id,
				'hide': option.hide.id,
				'show': option.show.id
			})

		return result

	def load(self, dictionary, pool):
		self.id = dictionary['id']

		for option_data in dictionary['options']:
			option = Option()
			option.description = option_data['description']
			option.available = option_data['available']
			option.message = option_data['message']
			option.triggers = pool.get_event(option_data['triggers'])
			option.hide = pool.get_event(option_data['hide'])
			option.show = pool.get_event(option_data['show'])
			self.options.append(option)

	def add_option(self):
		option = Option()
		self.options.append(option)
		return option

	def get_option(self, index):
		return self.options[index]

	def delete_option(self, index):
		del self.options[index]

	def get_options(self):
		return [option for option in self.options if option.is_available]

	def start_listening(self):
		for option in self.options:
			option.start_listening()

	def __repr__(self):
		return f"Conversation #{self.id} with {len(self.options)} Options"


class Option:
	def __init__(self):
		self.description = ""
		self.available = True  # by default
		self.message = ""
		self.triggers = nulls.event
		self.hide = nulls.event
		self.show = nulls.event

		self.is_available = self.available

	def wrap_for_editing(self, pool):
		return OptionEditor(self, pool)

	def start_listening(self):
		self.hide.subscribe(self)
		self.show.subscribe(self)

	def notify(self, event):
		if event == self.show:
			self.is_available = True
		elif event == self.hide:
			self.is_available = False
		else:
			raise Exception(
				"An option is notified about event that's not subscribed to."
			)

	def __repr__(self):
		return f"Option ({self.description[:10]}…)"
