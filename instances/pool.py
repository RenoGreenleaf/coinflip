from sqlalchemy import select
from reusables.session import Session
from event.models import Event, Irrelevant


def get_all_events():
	return events


def update_event(event):
	with Session() as session:
		session.add(event)
		session.commit()


#  the following script is expected to be executed on (first) import.
with Session() as session:
	events = session.scalars(select(Event)).all() + [Irrelevant()]
