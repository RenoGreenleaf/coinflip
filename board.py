# Copyright (C) 2026  Reno Greenleaf
from protocols import Player


class Piece:
	"""
	Implements all interfaces for any player might need from a piece.

	So that various piece types don't need to do it again
	and only have to implement what is relevant for them.
	"""

	def __init__(self):
		self.subscribers = set()
		self.children = []

	def load(self, raw: dict, relationships: dict):
		for identifier, raw_child in raw.get('children', {}).items():
			type_ = raw_child.get('type', 'piece')
			child = self.instantiate_child(type_)
			relationships[identifier] = child
			child.load(raw_child, relationships)
			self.children.append(child)

	def save(self):
		return {}

	def act(self, input_: int):
		pass

	def instantiate_child(self, type_: str):
		mapping = {
			'option': Option,
			'piece': Piece,
		}
		return mapping[type_]()

	def subscribe(self, player: Player):
		self.subscribers.add(player)

	def trigger(self):
		for subscriber in self.subscribers:
			subscriber.process(self)

	def __hash__(self):
		"""Make it usable as dictionary key."""
		return hash(id(self))


class World(Piece):
	"""Majority of game objects reside here."""

	def __init__(self):
		"""Define initial properties to be sure they're available later."""
		super().__init__()
		self.selected = Piece()

	def save(self):
		return {}

	def select(self, offset):
		options = self._get_for_player()
		self.selected = options[int(offset) - 1]

		if not self.selected.permanent:
			self.selected.hidden = True

		self.selected.trigger()

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
			for option in self.children
			if not option.hidden
		]


class Option(Piece):
	def __init__(self):
		super().__init__()

		self.description = ""
		self.message = ""
		self.permanent = False
		self.hidden = True


	def load(self, raw: dict, relationships: dict):
		self.description = raw['description']
		self.message = raw['message']
		self.permanent = raw['permanent']
		self.hidden = raw['hidden']

	def save(self):
		return {
			'description': self.description,
			'message': self.message,
			'permanent': self.permanent,
			'hidden': self.hidden,
		}


class Event(Piece):
	"""
	Special case, this one is outside a board.
	Represents a turn or a time tick.
	"""
