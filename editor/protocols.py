# Copyright (C) 2026  Reno Greenleaf
from typing import Literal, Protocol


class Node(Protocol):
	"""Board piece in editor."""

	type: str

	@property
	def children(self) -> list['Node']:
		"""For tree representation."""
		...

	def __str__(self) -> str:
		"""Show a title."""
		...
