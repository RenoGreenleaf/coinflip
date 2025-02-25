from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, ForeignKey
from reusables.models import Model, Scene
from event.models import Event
from state_machine.editor import Editor


class StateMachine(Model):
	__tablename__ = 'state_machine'
	id = mapped_column(Integer, primary_key=True)
	transitions = relationship(
		'Transition',
		back_populates='state_machine',
		lazy='selectin',
		cascade='all, delete-orphan'
	)

	def wrap_for_editing(self, pool):
		return Editor(self, pool)

	def add_transition(self, scene_id, event_id):
		self.transitions.append(Transition(scene_id=scene_id, event_id=event_id))

	def __repr__(self):
		count = len(self.transitions)
		return f"State machine #{self.id} with {count} transitions."


class Transition(Model):
	__tablename__ = 'transition'
	id = mapped_column(Integer, primary_key=True)
	event_id = mapped_column(ForeignKey(Event.id))
	scene_id = mapped_column(ForeignKey(Scene.id))
	state_machine_id = mapped_column(ForeignKey(StateMachine.id))

	event = relationship(Event, lazy='joined', foreign_keys=event_id)
	scene = relationship(Scene, lazy='joined', foreign_keys=scene_id)
	state_machine = relationship(
		StateMachine,
		lazy='joined',
		back_populates='transitions',
		foreign_keys=state_machine_id
	)

	def __repr__(self):
		return f"To {self.scene} by {self.event}"
