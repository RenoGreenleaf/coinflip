from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Model(DeclarativeBase):
	"""Holds DB metadata."""


class Scene(Model):
	__tablename__ = 'scene'
	id = mapped_column(Integer(), primary_key=True)
	type = mapped_column(String())

	__mapper_args__ = {
		'polymorphic_identity': 'scene',
		'polymorphic_on': 'type'
	}

	def start_listening(self):
		pass

	def notify(self):
		pass

	def wrap_for_editing(self, pool):
		raise Exception("Dead-end can't be edited.")

	def wrap_for_playing(self, pool):
		raise Exception("Dead-end isn't playable.")

	def __repr__(self):
		return "<Dead-end>"
