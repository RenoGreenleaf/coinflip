from dataclasses import dataclass
from types import MappingProxyType


@dataclass
class Message:
	"""It's meant to be sent to a world and be processed by it."""

	text: str = ""
	actions: dict = MappingProxyType({})

	def save(self):
		return {}

	def load(self, json):
		self.text = json['text']
		self.actions = MappingProxyType(json['actions'])


class World:
	"""Majority of game objects reside here."""

	def get_option(self):
		key = input("> ")
		return self.options.get(key, EmptyOption())

	def process(self, message):
		self._print("---------------")
		self._print(message.text)
		print()

		self._remove(message)

		for option in self.options.values():
			self._print(option)

	def save(self):
		return {}

	def load(self, json):
		self.options = {}

		for key, raw_option in json.items():
			option = Option()
			option.load(raw_option)
			self.options[key] = option

	def _remove(self, message):
		to_remove = message.actions.get('remove', [])

		for key in to_remove:
			self.options.pop(key)

	def _print(self, text):
		if text != "":
			print(text)


class Option:
	"""Represents what can be done at the moment."""

	def get_message(self):
		return self.message

	def save(self):
		return {}

	def load(self, json):
		self.description = json['description']
		self.message = Message()
		self.message.load(json['message'])

	def __repr__(self):
		return self.description


class EmptyOption:
	def get_message(self):
		return Message()