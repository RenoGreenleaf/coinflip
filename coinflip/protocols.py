# Copyright (C) 2026  Reno Greenleaf
from typing import Protocol


class Player(Protocol):
	"""Uses a board."""

	def process(self, event: 'Event'):
		"""Make a turn."""


class Event(Protocol):
	"""Animates players."""

	def subscribe(self, player: Player):
		"""Make a player listen to it."""

	def trigger(self):
		"""Let listeners know that the event has occurred."""

	def __hash__(self) -> int:
		"""Make it usable as dict key."""
		return 0


class Persistent(Protocol):
	"""Can be saved."""

	def persist(self, relationships: dict):
		"""Preserve current piece for further references."""
