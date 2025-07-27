from dataclasses import dataclass


@dataclass
class Message:
	"""It's meant to be sent to a world and be processed by it."""

	text: str = ""


class World:
	"""Majority of game objects reside here."""

	def get_option(self):
		key = input("> ")

		if key not in self.options:
			option = Option()
			option.load({'text': "Unclear", 'description': ""})
			return option

		return self.options[key]

	def process(self, message):
		print("---------------")
		print(message.text, "\n")

		for option in self.options.values():
			print(option)

	def save(self):
		return {}

	def load(self, json):
		self.options = {}

		for key, raw_option in json.items():
			option = Option()
			option.load(raw_option)
			self.options[key] = option


class Option:
	"""Represents what can be done at the moment."""

	def get_message(self):
		return Message(text=self.text)

	def save(self):
		return {}

	def load(self, json):
		self.text = json['text']
		self.description = json['description']

	def __repr__(self):
		return self.description
