# Copyright (C) 2026  Reno Greenleaf
from coinflip.pieces import Piece
from typing import Literal, cast
from editor import protocols


class Option(Piece):
	type: Literal['option']
	description: str = ""
	message: str = ""
	permanent: bool = False
	hidden: bool = True

	def describe(self, value: str):
		self.description = value

	def __str__(self) -> str:
		return self.description


class Conversation(Piece):
	type: Literal['conversation']
	options: list[Option]
	subject: str

	def persist(self, relationships: dict):
		relationships[str(self.identifier)] = self

		for option in self.options:
			option.persist(relationships)

	@property
	def children(self) -> list[protocols.Node]:
		return cast(list[protocols.Node], self.options)

	def __str__(self) -> str:
		return self.subject
