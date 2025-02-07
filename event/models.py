from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column
from reusables.model import Model


class Event(Model):
	__tablename__ = 'event'

	id = mapped_column(Integer(), primary_key=True)
	name = mapped_column(String(255), nullable=False)

	def __repr__(self):
		return self.name


class Irrelevant:
	# TODO: make it a model, so that it, instead of NULL, is stored.
	"""
	Empty event, it supposed to be triggered by default.
	It's for Null Object pattern.
	"""

	def __repr__(self):
		return '<Irrelevant>'
