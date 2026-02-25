# Copyright (C) 2026  Reno Greenleaf
from coinflip.pieces import Piece
from typing import Literal


class Option(Piece):
	type: Literal['option']
	description: str = ""
	message: str = ""
	permanent: bool = False
	hidden: bool = True

	def __str__(self):
		return self.description


class Conversation(Piece):
	type: Literal['conversation']
	options: list[Option]
	subject: str

	def persist(self, relationships):
		relationships[str(self.identifier)] = self

		for option in self.options:
			option.persist(relationships)

	@property
	def children(self):
		return self.options

	def __str__(self):
		return self.subject
