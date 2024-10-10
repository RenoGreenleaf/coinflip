from json import load
from event.event import Event, Irrelevant


events = {'none': Irrelevant()}

with open('instances/events.json') as events_data:
	keys = set(load(events_data))

for key in keys:
	events[key] = Event()
