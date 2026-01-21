# Copyright (C) 2026  Reno Greenleaf
"""All in one."""


class Outer:
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
		for connection in json['ai']:
			event = relationships.get('event', connection['trigger'])
			option = relationships.get('option', connection['affected'])
			action = self._hide if connection['action'] == 'hide' else self._show
			self.connections.setdefault(event, []).append((action, option))

			event.subscribe(self)

	def _hide(self, option):
		option.hidden = True

	def _show(self, option):
		option.hidden = False

	def save(self):
		return {}


class Event:
	def __init__(self):
		"""Define initial properties to be sure they're available later."""
		self.subscribers = set()

	def subscribe(self, subscriber):
		self.subscribers.add(subscriber)

	def trigger(self):
		for subscriber in self.subscribers:
			subscriber.process(self)

	def __hash__(self):
		"""Make it usable as dictionary key."""
		return hash(id(self))


class Option:

	def __init__(self):
		"""Define initial properties to be sure they're available later."""
		self.description = ""
		self.message = ""
		self.permanent = False
		self.hidden = True

		self.subscribers = set()

	def load(self, json, relationships):
		self.description = json['description']
		self.message = json['message']
		self.permanent = json['permanent']
		self.hidden = json['hidden']

	def save(self):
		return {
			'description': self.description,
			'message': self.message,
			'permanent': self.permanent,
			'hidden': self.hidden,
		}

	def subscribe(self, subscriber):
		self.subscribers.add(subscriber)

	def trigger(self):
		for subscriber in self.subscribers:
			subscriber.process(self)

	def __hash__(self):
		"""Make it usable as dictionary key."""
		return hash(id(self))


class World:
	"""Majority of game objects reside here."""
	def __init__(self):
		"""Define initial properties to be sure they're available later."""
		self.available = {}
		self.selected = Option()
		self.cleared = False

	def load(self, json, relationships):
		for identifier, raw_option in json['available'].items():
			option = Option()
			option.load(raw_option, relationships)
			self.available[identifier] = option

	def save(self):
		return {}

	def select(self, offset):
		options = self._get_for_player()
		self.selected = options[int(offset) - 1]

		if not self.selected.permanent:
			self.selected.hidden = True

		self.selected.trigger()

	def get(self, key, identifier):
		if key != 'option' and key != 'event':
			raise KeyError()

		return self.available.get(identifier, Option())

	def unid(self, key):
		if key != 'option' and key != 'event':
			raise KeyError()

		if not self.cleared:
			self.available = list(self.available.values())
			self.cleared = True

	def __getattribute__(self, name):
		if name == 'message':
			return self.selected.message
		elif name == 'description':
			return self._get_description()
		else:
			return super().__getattribute__(name)

	def _get_description(self):
		descriptions = []
		offset = 0

		for option in self._get_for_player():
			offset += 1
			descriptions.append(str(offset) + ". " + option.description)

		return "\n".join(descriptions)

	def _get_for_player(self):
		return [
			option
			for option in self.available
			if not option.hidden
		]
