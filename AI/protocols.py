from typing import Protocol


class Node(Protocol):
	"""Element of AI player reasoning."""

	def act(self, input_: int):
		"""Micro decision."""
