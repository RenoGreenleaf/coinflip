from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from event.models import Event, Irrelevant


def get_all_events():
	return events


#  the following script is expected to be executed on (first) import.
engine = create_engine('sqlite:///db.sqlite3')

with Session(engine) as session:
	events = session.scalars(select(Event)).all() + [Irrelevant()]
