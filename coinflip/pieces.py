# Copyright (C) 2026  Reno Greenleaf
from pydantic import BaseModel
from coinflip.protocols import Player
from editor.protocols import Node


class Piece(BaseModel):
	"""
	Implements all interfaces for any player might need from a piece.

	So that various piece types don't need to do it again
	and only have to implement what is relevant for them.
	"""

	identifier: int = 0
	_subscribers: set = set()

	def act(self, input_: int) -> None:
		pass

	def subscribe(self, player: Player) -> None:
		self._subscribers.add(player)

	def trigger(self) -> None:
		for subscriber in self._subscribers:
			subscriber.process(self)

	def persist(self, relationships: dict[str, 'Piece']) -> None:
		relationships[str(self.identifier)] = self

	@property
	def children(self) -> list[Node]:
		return []

	def describe(self, value: str):
		pass

	def __hash__(self) -> int:
		"""Make it usable as dictionary key."""
		return hash(id(self))

	def __str__(self) -> str:
		return '<no title>'


class Event(Piece):
	"""
	Special case, this one is outside a board.

	Represents a turn or a time tick.
	"""
