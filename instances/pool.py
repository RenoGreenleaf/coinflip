from sqlalchemy import select
from reusables.session import Session
from reusables.models import Scene
from event.models import Event, Irrelevant
from instances.editor import Editor


class Pool:
	def __init__(self):
		self.events = []
		self.scenes = []

	def get_all_events(self):
		return self.events

	def update_event(self, event):
		with Session() as session:
			session.add(event)
			session.commit()

	def update(self):
		"""Makes pool up to date with last changes."""
		with Session() as session:
			self.events = [Irrelevant()] + session.scalars(select(Event)).all()
			self.scenes = session.scalars(select(Scene)).all()

	def wrap_for_editing(self):
		keyed = {
			'events': {event.id: event for event in self.events},
			'scenes': {scene.id: scene for scene in self.scenes}
		}
		return Editor(keyed)
