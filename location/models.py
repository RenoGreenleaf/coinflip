from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from reusables.models import Scene, Model
from event.models import Event
from location.editor import Editor
from location.player import Player


class Location(Scene):
	"""Things to explore."""

	__tablename__ = 'location'
	__mapper_args__ = {
		'polymorphic_identity': 'location',
		'polymorphic_load': 'selectin'
	}
	id = mapped_column(ForeignKey(Scene.id), primary_key=True)
	description = mapped_column(String())
	exits = relationship(
		'Exit',
		back_populates='location',
		lazy='selectin',
		cascade='all, delete-orphan'
	)

	discovered_event_id = mapped_column(ForeignKey(Event.id))
	discovered_event = relationship(
		Event,
		lazy='joined'
	)

	def wrap_for_editing(self, pool):
		return Editor(self, pool)

	def wrap_for_playing(self, pool):
		return Player(self, pool)

	def find_exits(self, startswith):
		return [exit_ for exit_ in self.exits if exit_.name.startswith(startswith)]

	def find_exit_by_name(self, name):
		exits = [exit_ for exit_ in self.exits if exit_.name == name]

		if exits:
			return exits[0]
		else:
			raise Exception(f"There's no exit named {name}")

	def add_exit(self, name, triggers_event_id=None):
		self.exits.append(Exit(name=name, triggers_event_id=triggers_event_id))

	def set_discovered_event(self, identifier):
		self.discovered_event_id = identifier

	def delete_exit(self, identifier):
		for exit_ in self.exits:
			if exit_.id == identifier:
				to_delete = exit_
				break

		self.exits.remove(to_delete)

	def __repr__(self):
		return f"Location ({self.description[:15]}…)"


class Exit(Model):
	__tablename__ = 'location_exit'
	id = mapped_column(Integer(), primary_key=True)
	location_id = mapped_column(ForeignKey(Location.id))
	name = mapped_column(String(255))  # for usage in command prompt commands
	description = mapped_column(String())
	location = relationship(
		Location,
		back_populates='exits',
		foreign_keys=(location_id),
		lazy='joined'
	)
	triggers_event_id = mapped_column(ForeignKey(Event.id))
	triggers_event = relationship(Event, lazy='joined')

	def __repr__(self):
		return f"Exit ({self.name})"
