from sqlalchemy import select
from reusables.session import Session
from reusables.models import Scene
from event.models import Event
from state_machine.models import StateMachine
from instances.editor import Editor


class Pool:
	def __init__(self):
		self.editor = None
		self.scenes = []
		self.events = []

		with self.get_db_session() as session:
			self.state_machine = session.scalars(select(StateMachine)).one_or_none()

			if self.state_machine is None:
				self.state_machine = StateMachine()
				session.add(self.state_machine)
				session.commit()

	def get_all_events(self):
		with self.get_db_session() as session:
			session.add_all(self.events)
			self.events = session.scalars(select(Event)).all()
			return self.events

	def get_all_scenes(self):
		with self.get_db_session() as session:
			session.add_all(self.scenes)
			self.scenes = session.scalars(select(Scene)).all()
			return self.scenes

	def get_event(self, identifier):
		with self.get_db_session() as session:
			session.add_all(self.scenes)
			return session.get(Event, identifier)

	def get_scene(self, identifier):
		with self.get_db_session() as session:
			session.add_all(self.scenes)
			return session.get(Scene, identifier)

	def get_state_machine(self):
		with self.get_db_session() as session:
			session.add(self.state_machine)
			return session.scalars(select(StateMachine)).one()

	def wrap_for_editing(self, pool):
		if not self.editor:
			self.editor = Editor(pool)

		return self.editor

	def get_db_session(self):
		return Session()
