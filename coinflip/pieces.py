from pydantic import BaseModel, Field, TypeAdapter
from typing import Annotated
from coinflip.protocols import Player


class Piece(BaseModel):
	"""
	Implements all interfaces for any player might need from a piece.

	So that various piece types don't need to do it again
	and only have to implement what is relevant for them.
	"""

	identifier: int
	_subscribers: set = set()
	_children: list = []

	def load(self, raw: dict, relationships: dict):
		from terminal.pieces import Option  # it's here to prevent circular imports
		adapter = TypeAdapter(
			Annotated[Option, Field(discriminator='type')]
		)

		for raw_child in raw.get('children', []):
			child = adapter.validate_python(raw_child)
			relationships[str(child.identifier)] = child
			self._children.append(child)

	def save(self):
		return {}

	def act(self, input_: int):
		pass

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
