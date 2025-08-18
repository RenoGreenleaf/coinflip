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
			actions[function] = argument

		self.actions = MappingProxyType(actions)


class World:
	"""Majority of game objects reside here."""

	def __init__(self):
		self.callbacks = {}
		self.options = {}

	def get_option(self):
		command = input("> ")

		for option in self.options.values():
			if option.matches(command):
				return option

		return EmptyOption()

	def process(self, message):
		self._print("---------------")
		self._print(message.text)
		print()

		for function, argument in message.actions.items():
			function(argument)

		for option in self.options.values():
			self._print(option)

	def save(self):
		return {}

	def load(self, json, relationships):
		self.callbacks['hide'] = self._hide

		for key, raw_option in json.items():
			option = Option()
			option.load(raw_option, self)
			self.options[key] = option

	def set(self, key, identifier, value):
		if key == 'callback':
			self.callbacks[identifier] = value
		else:
			raise Exception("The key isn't supported.")

	def get(self, key, identifier):
		if key == 'callback':
			return self.callbacks[identifier]
		else:
			raise Exception("The key isn't supported.")

	def _hide(self, options):
		for identifier in options:
			self.options.pop(identifier)

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



class EmptyRelationships:
	def set(self, key, identifier, value):
		pass

	def get(self, key, identifier):
		pass