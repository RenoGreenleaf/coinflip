from dataclasses import dataclass
from types import MappingProxyType


@dataclass
class Message:
	"""It's meant to be sent to a world and be processed by it."""

	text: str = ""
	actions: dict = MappingProxyType({})

	def save(self):
		return {}

	def load(self, json, relationships):
		self.text = json['text']
		actions = {}

		for name, argument in json['actions'].items():
			function = relationships.get('callback', name)
			loaded_argument = self._load_argument(name, argument, relationships)
			actions[function] = loaded_argument

		self.actions = MappingProxyType(actions)

	def _load_argument(self, callback, argument, relationships):
		if callback == 'hide' or callback == 'show':
			return list(self._load_options(argument, relationships))

	def _load_options(self, ids, relationships):
		for identifier in ids:
			yield relationships.get('option', identifier)


class World:
	"""Majority of game objects reside here."""

	def __init__(self):
		self.callbacks = {}
		self.options = {}
		self.hidden = {}

	def get_option(self):
		command = input("> ")

		for option in self.options:
			if option.matches(command):
				return option

		return EmptyOption()

	def process(self, message):
		self._print("---------------")
		self._print(message.text)
		print()

		for function, argument in message.actions.items():
			function(argument)

		for option in self.options:
			self._print(option)

	def save(self):
		return {}

	def load(self, json, relationships):
		self.callbacks = {
			'hide': self._hide,
			'show': self._show
		}

		for key in json['available']:
			self.options[key] = Option()

		for key in json['hidden']:
			self.hidden[key] = Option()

		for key, option in self.options.items():
			option.load(json['available'][key], relationships)

		for key, option in self.hidden.items():
			option.load(json['hidden'][key], relationships)

	def set(self, key, identifier, value):
		if key == 'callback':
			self.callbacks[identifier] = value
		else:
			raise Exception("The key isn't supported.")

	def get(self, key, identifier):
		if key == 'callback':
			return self.callbacks[identifier]
		elif key == 'option':
			return self.options.get(identifier, self.hidden.get(identifier))
		else:
			raise Exception("The key isn't supported.")

	def unid(self):
		self.options = list(self.options.values())
		self.hidden = list(self.hidden.values())
		del self.callbacks

	def _hide(self, options):
		for option in options:
			self.options.remove(option)
			self.hidden.append(option)

	def _show(self, options):
		for option in options:
			self.hidden.remove(option)
			self.options.append(option)

	def _print(self, text):
		if text != "":
			print(text)


class Option:
	"""Represents what can be done at the moment."""

	def get_message(self):
		return self.message

	def save(self):
		return {}

	def load(self, json, relationships):
		self.description = json['description']
		self.pattern = json['pattern']
		self.message = Message()
		self.message.load(json['message'], relationships)

	def __repr__(self):
		return self.description

	def matches(self, text):
		return self.pattern == text


class EmptyOption:
	def get_message(self):
		return Message()
