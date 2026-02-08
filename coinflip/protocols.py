# Copyright (C) 2026  Reno Greenleaf
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


class Persistent(Protocol):
	"""Can be saved."""

	def load(self, raw: dict, relationships: dict):
		"""Populate self with data from raw."""

	def save(self):
		"""Create raw data from self."""
