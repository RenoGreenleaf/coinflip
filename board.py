# Copyright (C) 2026  Reno Greenleaf


class Piece:
	"""
	Implements all interfaces for any player might need from a piece

	so that various piece types don't need to do it again
	and only have to implement what is relevant for them.
	"""

	def __init__(self):
		self.subscribers = set()
		self.children = []

	def load(self, raw, relationships):
		for raw_child in raw.get('children', {}).values():
			type_ = raw_child.get('type', 'piece')
			child = self.instantiate_child(type_)
			child.load(raw_child, relationships)
			self.children.append(child)

	def save(self):
		return {}

	def act(self, input_):
		pass

	def instantiate_child(self, type_):
		mapping = {
			'option': Option,
			'piece': Piece,
		}
		return mapping[type_]()

	def subscribe(self, subscriber):
		self.subscribers.add(subscriber)

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

		self.available = {}
		self.selected = Piece()
		self.cleared = False

	def load(self, raw, relationships):
		super().load(raw, relationships)

		for identifier, raw_piece in raw['available'].items():
			option = Option()
			option.load(raw_piece, relationships)
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
			self.children = list(self.available.values())
			self.available = {}
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


class Event(Piece):
	"""
	Special case, this one is outside a board.
	Represents a turn or a time tick.
	"""
