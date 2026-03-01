# Copyright (C) 2026  Reno Greenleaf
from typing import Literal, Protocol


class Node(Protocol):
	"""Board piece in editor."""

	type: str

	@property
	def children(self) -> list['Node']:
		"""For tree representation."""
		...

	def describe(self, value: str):
		"""Set value to be used by __str__()."""

	def __str__(self) -> str:
		"""Show a title."""
		...
