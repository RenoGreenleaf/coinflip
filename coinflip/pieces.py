# Copyright (C) 2026  Reno Greenleaf
from pydantic import BaseModel
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

	def save(self):
		return {}

	def act(self, input_: int):
		pass

	def subscribe(self, player: Player):
		self._subscribers.add(player)

	def trigger(self):
		for subscriber in self._subscribers:
			subscriber.process(self)

	def persist(self, relationships):
		relationships[str(self.identifier)] = self

	@property
	def children(self):
		return []

	def __hash__(self):
		"""Make it usable as dictionary key."""
		return hash(id(self))

	def __str__(self):
		return '<no title>'


class Event(Piece):
	"""
	Special case, this one is outside a board.

	Represents a turn or a time tick.
	"""
