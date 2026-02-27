# Copyright (C) 2026  Reno Greenleaf
from coinflip.protocols import Event


class System:
	"""A player making decisions using system input/output."""

	def __init__(self, world):
		"""Define initial properties to be sure they're available later."""
		self.world = world

	def process(self, event: Event):
		options = list(self._get_options())

		for index, option in enumerate(options):
			print(f"{index + 1}. {option.description}")

		offset = input('> ')

		if offset == 'exit':
			exit()

		option = options[int(offset) - 1]
		self.world.select(option)
		print(option.message)

	def load(self, raw: dict, relationships: dict):
		"""Implement persistent interface."""

	def save(self) -> dict:
		"""Implement persistent interface."""
		return {}

	def _get_description(self) -> str:
		descriptions = []
		offset = 0

		for option in self._get_options():
			offset += 1
			descriptions.append(str(offset) + ". " + option.description)

		return "\n".join(descriptions)

	def _get_options(self):
		conversation = self.world.conversations[0]

		for option in conversation.options:
			if not option.hidden:
				yield option
