# Copyright (C) 2026  Reno Greenleaf
from pydantic import Field
from typing import Annotated, Literal
from coinflip.pieces import Piece
from terminal.pieces import Option


AnyPiece = Annotated[Option, Field(discriminator='type')]


class World(Piece):
	"""Majority of game objects reside here."""

	_selected: Piece
	type: Literal['world']
	children: list[AnyPiece]

	def select(self, piece):
		self._selected = piece

		if not self._selected.permanent:
			self._selected.hidden = True

		self._selected.trigger()

	def persist(self, relationships):
		relationships[str(self.identifier)] = self

		for child in self.children:
			child.persist(relationships)
