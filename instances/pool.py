from sqlalchemy import select
from reusables.session import Session
from reusables.models import Scene
from event.models import Event
from instances.editor import Editor


class Pool:
	def __init__(self):
		self.editor = None

	def get_all_events(self):
		with self.get_db_session() as session:
			return session.scalars(select(Event)).all()

	def get_all_scenes(self):
		with self.get_db_session() as session:
			return session.scalars(select(Scene)).all()

	def get_event(self, identifier):
		with self.get_db_session() as session:
			return session.get(Event, identifier)

	def get_scene(self, identifier):
		with self.get_db_session() as session:
			return session.get(Scene, identifier)

	def wrap_for_editing(self, pool):
		if self.editor:
			self.editor.update_pool(pool)
		else:
			self.editor = Editor(pool)

		return self.editor

	def get_db_session(self):
		return Session()
