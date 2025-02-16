from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from reusables.models import Scene, Model
from room.editor import Editor


class Room(Scene):
	"""Things to explore."""

	__tablename__ = 'room'
	__mapper_args__ = {
		'polymorphic_identity': 'room',
		'polymorphic_load': 'selectin'
	}
	id = mapped_column(ForeignKey('scene.id'), primary_key=True)
	description = mapped_column(String())
	exits = relationship('Exit', back_populates='room', lazy='selectin')

	def wrap_for_editing(self):
		return Editor(self)

	def __repr__(self):
		return f"Room ({self.description[:15]}…)"


class Exit(Model):
	__tablename__ = 'room_exit'
	id = mapped_column(Integer(), primary_key=True)
	room_id = mapped_column(ForeignKey('room.id'))
	name = mapped_column(String(255))  # for usage in command prompt commands
	room = relationship(
		Room,
		back_populates='exits',
		foreign_keys=(room_id),
		lazy='joined'
	)

	def __repr__(self):
		return f"Exit ({self.name})"
