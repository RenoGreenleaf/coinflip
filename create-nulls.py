"""Implements null object pattern."""
from reusables.session import Session
from event.models import Event


with Session() as session:
	event = Event(id=0, name="<Irrelevant>")
	session.merge(event)
	session.commit()
