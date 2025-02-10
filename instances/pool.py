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


def wrap_for_editing():
	with_keys = {event.id: event for event in events}
	return Editor(with_keys)


#  the following script is expected to be executed on (first) import.
with Session() as session:
	events = [Irrelevant()] + session.scalars(select(Event)).all()
