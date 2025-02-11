from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Model(DeclarativeBase):
	"""Holds DB metadata."""


class Scene(Model):
	__tablename__ = 'scene'
	id = mapped_column(Integer(), primary_key=True)
	name = mapped_column(String())
	type = mapped_column(String())

	__mapper_args__ = {
		'polymorphic_identity': 'scene',
		'polymorphic_on': 'type'
	}

	def __repr__(self):
		return f"{self.__class__.__name__}({self.name!r})"
