# Copyright (C) 2026  Reno Greenleaf
from pydantic import Field, TypeAdapter
from typing import Annotated
from coinflip.pieces import Piece
from terminal.pieces import Option


AnyPiece = Annotated[Option, Field(discriminator='type')]


class World(Piece):
	"""Majority of game objects reside here."""

	_selected: Piece
	children: list[AnyPiece]

	def select(self, piece):
		self._selected = piece

		if not self._selected.permanent:
			self._selected.hidden = True

		self._selected.trigger()

	def load(self, raw: dict, relationships: dict):
		adapter = TypeAdapter(AnyPiece)

		for raw_child in raw.get('children', []):
			child = adapter.validate_python(raw_child)
			relationships[str(child.identifier)] = child
			self.children.append(child)
