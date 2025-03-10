"""Implements null object pattern."""
from reusables.session import Session
from reusables.models import Scene
from event.models import Event


with Session() as session:
	event = Event(id=0, name="<Irrelevant>")
	scene = Scene(id=0)
	session.merge(event)
	session.merge(scene)
	session.commit()
