from typing import Protocol


class Player(Protocol):
	"""Uses a board."""

	def process(self, event):
		"""Make a turn."""


class Event(Protocol):
	"""Animates players."""

	def subscribe(self, player: Player):
		"""Make a player listen to it."""

	def trigger(self):
		"""Let listeners know that the event has occurred."""

	def __hash__(self):
		"""Make it usable as dict key."""


class Relationships(Protocol):
	"""Helps to fetch objects specified by IDs (like foreign keys)."""

	def get(self, key: str, identifier: str):
		"""Obtain already loaded object."""

	def unid(self, key: str):
		"""Cleanup."""


class Persistent(Protocol):
	"""Can be saved."""

	def load(self, raw: dict, relationships: Relationships):
		"""Populate self with data from raw."""

	def save(self):
		"""Create raw data from self."""


class Node(Protocol):
	"""Element of AI player reasoning."""

	def act(self, input_: int):
		"""Micro decision."""
