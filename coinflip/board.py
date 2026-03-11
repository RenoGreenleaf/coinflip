# Copyright (C) 2026  Reno Greenleaf
from typing import Literal, cast
from coinflip.pieces import Piece
from editor.protocols import Node
from terminal.pieces import Conversation


# AnyPiece = Annotated[Option, Field(discriminator='type')]


class World(Piece):
	"""Majority of game objects reside here."""

	_selected: Piece
	type: str = 'world'
	conversations: list[Conversation] = []

	def select(self, piece):
		self._selected = piece

		if not self._selected.permanent:
			self._selected.hidden = True

		self._selected.trigger()

	def persist(self, relationships):
		relationships[str(self.identifier)] = self

		for conversation in self.conversations:
			conversation.persist(relationships)

	@property
	def children(self) -> list[Node]:
		return cast(list[Node], self.conversations)

	def __str__(self):
		return "World"
