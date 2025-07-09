from dataclasses import dataclass


@dataclass
class Message:
	"""It's meant to be sent to a world and be processed by it."""

	text: str = ""


class World:
	"""Majority of game objects reside here."""

	def get_option(self):
		input()
		return Option()

	def process(self, message):
		print(message.text)


class Option:
	"""Represents what can be done at the moment."""

	def get_message(self):
		return Message(text="Hello, world!")
