from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column
from reusables.models import Model
from event.editor import Editor


class Event(Model):
	__tablename__ = 'event'

	id = mapped_column(Integer(), primary_key=True)
	name = mapped_column(String(255), nullable=False)

	def __repr__(self):
		return self.name

	def wrap_for_editing(self, pool):
		return Editor(self, pool)


class Irrelevant:
	# TODO: make it a model, so that it, instead of NULL, is stored.
	"""
	Empty event, it supposed to be triggered by default.
	It's for Null Object pattern.
	"""
	id = ''

	def __repr__(self):
		return '<Irrelevant>'

	def wrap_for_editing(self):
		return Editor(self)
