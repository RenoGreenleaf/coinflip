# Copyright (C) 2026  Reno Greenleaf
from coinflip.pieces import Piece
from typing import Literal


class Option(Piece):
	type: Literal['option']
	description: str = ""
	message: str = ""
	permanent: bool = False
	hidden: bool = True


class Conversation(Piece):
	type: Literal['conversation']
	options: list[Option]

	def persist(self, relationships):
		relationships[str(self.identifier)] = self

		for option in self.options:
			option.persist(relationships)
