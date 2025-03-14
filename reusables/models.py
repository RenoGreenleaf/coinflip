from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, mapped_column
from reusables.nulls import Editor, Player


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
		return Editor(self, pool)

	def wrap_for_playing(self, pool):
		return Player(self, pool)

	def __repr__(self):
		if self.id == 0:
			return "<Dead-End>"
		else:
			return "Nameless"
