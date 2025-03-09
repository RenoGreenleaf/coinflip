from sqlalchemy.orm import mapped_column, relationship, reconstructor
from sqlalchemy import Integer, ForeignKey, inspect
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
	start_id = mapped_column(ForeignKey(Scene.id), nullable=False, default=0)
	start = relationship(Scene, lazy='joined')

	@reconstructor
	def load(self):
		self.current_scene = self.start

	def start_listening(self):
		for transition in self.transitions:
			transition.event.subscribe(self)

	def notify(self, triggered_event):
		for transition in self.transitions:
			if transition.event == triggered_event:
				self.current_scene = transition.scene
				break

	def get_current_scene(self):
		return self.current_scene

	def wrap_for_editing(self, pool):
		return Editor(self, pool)

	def add_transition(self, scene_id, event_id):
		self.transitions.append(Transition(scene_id=scene_id, event_id=event_id))

	def delete_transition(self, identifier):
		session = inspect(self).session
		transition = session.get(Transition, identifier)
		session.delete(transition)
		session.commit()

	def set_start(self, scene_id):
		self.start_id = scene_id

	def __repr__(self):
		count = len(self.transitions)
		return f"State machine #{self.id} with {count} transitions."


class Transition(Model):
	__tablename__ = 'transition'
	id = mapped_column(Integer, primary_key=True)
	event_id = mapped_column(ForeignKey(Event.id), nullable=False)
	scene_id = mapped_column(ForeignKey(Scene.id), nullable=False)
	state_machine_id = mapped_column(ForeignKey(StateMachine.id), nullable=False)

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
