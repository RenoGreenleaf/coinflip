# Copyright (C) 2026  Reno Greenleaf

class System:
	"""A player making decisions using system input/output."""

	def __init__(self, world):
		"""Define initial properties to be sure they're available later."""
		self.world = world

	def process(self, event):
		print(self.world.description)
		offset = input('> ')

		if offset == 'exit':
			exit()

		self.world.select(offset)
		print(self.world.message)

	def load(self, json, relationships):
		"""Implement persistent interface."""

	def save(self):
		"""Implement persistent interface."""
		return {}


class AI:
	"""A player reacting to actual players actions."""

	def __init__(self, world):
		"""Define initial properties to be sure they're available later."""
		self.world = world
		self.connections = {}

	def process(self, event):
		for action, option in self.connections.get(event, []):
			action(option)

	def load(self, json, relationships):
		for connection in json['ai']['connections']:
			event = relationships.get('event', connection['trigger'])
			option = relationships.get('option', connection['affected'])
			action = self._hide if connection['action'] == 'hide' else self._show
			self.connections.setdefault(event, []).append((action, option))

			event.subscribe(self)

	def save(self):
		return {}

	def _hide(self, option):
		option.hidden = True

	def _show(self, option):
		option.hidden = False

