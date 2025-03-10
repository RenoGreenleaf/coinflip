from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, reconstructor
from reusables.models import Model
from reusables import nulls
from event.editor import Editor


class Event(Model):
	"""A message broadcasted when something happens.
	Helps to interact between decoupled parts of an app."""

	__tablename__ = 'event'
	id = mapped_column(Integer(), primary_key=True)
	name = mapped_column(String(255), nullable=False, default="")

	@reconstructor
	def prepare(self):
		self.subscribers = []

	def wrap_for_editing(self, pool):
		if self.id == 0:
			return nulls.Editor(self, pool)

		return Editor(self, pool)

	def subscribe(self, subscriber):
		"""Let event know whom to notify if it's triggered."""
		if self.id != 0:
			self.subscribers.append(subscriber)

	def trigger(self):
		"""Signifies that an event has happened."""
		for subscriber in self.subscribers:
			subscriber.notify(self)

	def __repr__(self):
		return self.name
