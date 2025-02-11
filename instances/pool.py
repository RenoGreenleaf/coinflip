from sqlalchemy import select
from reusables.session import Session
from event.models import Event, Irrelevant
from instances.editor import Editor


def get_all_events():
	return events


def update_event(event):
	with Session() as session:
		session.add(event)
		session.commit()


def update():
	"""Makes pool up to date with last changes."""
	global events

	with Session() as session:
		events = [Irrelevant()] + session.scalars(select(Event)).all()


def wrap_for_editing():
	with_keys = {event.id: event for event in events}
	return Editor(with_keys)
