from reusables.models import Scene
from conversation.editor import Editor, OptionEditor
from conversation.player import Player


class Conversation(Scene):
	def __init__(self):
		self.options = []

	def wrap_for_editing(self, pool):
		return Editor(self, pool)

	def wrap_for_playing(self, pool):
		return Player(self, pool)

	def add_option(self):
		option = Option()
		self.options.append(option)
		return option

	def get_option(self, identifier):
		for option in self.options:
			if option.id == identifier:
				return option

	def delete_option(self, identifier):
		for option in self.options:
			if option.id == identifier:
				self.options.remove(option)

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
		self.triggers = None
		self.hide = None
		self.show = None

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
