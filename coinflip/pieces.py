from pydantic import BaseModel
from coinflip.protocols import Player


class Piece(BaseModel):
	"""
	Implements all interfaces for any player might need from a piece.

	So that various piece types don't need to do it again
	and only have to implement what is relevant for them.
	"""

	_subscribers: set
	_children: list

	def __init__(self, **data):
		super().__init__(**data)
		self._subscribers = set()
		self._children = []

	def load(self, raw: dict, relationships: dict):
		for identifier, raw_child in raw.get('children', {}).items():
			type_ = raw_child.get('type', 'piece')
			child = self.instantiate_child(type_)
			relationships[identifier] = child
			child.load(raw_child, relationships)
			self._children.append(child)

	def save(self):
		return {}

	def act(self, input_: int):
		pass

	def instantiate_child(self, type_: str):
		from terminal.pieces import Option  # it's here to prevent circular imports

		mapping = {
			'option': Option,
			'piece': Piece,
		}
		return mapping[type_]()

	def subscribe(self, player: Player):
		self._subscribers.add(player)

	def trigger(self):
		for subscriber in self._subscribers:
			subscriber.process(self)

	@property
	def children(self):
		return self._children

	def __hash__(self):
		"""Make it usable as dictionary key."""
		return hash(id(self))


class World(Piece):
	"""Majority of game objects reside here."""

	_selected: Piece

	def __init__(self, **data):
		"""Define initial properties to be sure they're available later."""
		super().__init__(**data)
		self._selected = Piece()

	def select(self, piece):
		self._selected = piece

		if not self._selected.permanent:
			self._selected.hidden = True

		self._selected.trigger()


class Event(Piece):
	"""
	Special case, this one is outside a board.

	Represents a turn or a time tick.
	"""
