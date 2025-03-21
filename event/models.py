from event.editor import Editor


class Event:
	"""A message broadcasted when something happens.
	Helps to interact between decoupled parts of an app."""

	def __init__(self, **kwargs):
		self.id = 0
		self.name = ""

		self.subscribers = []

	def save(self):
		return {
			'id': self.id,
			'name': self.name
		}

	def load(self, dictionary, pool):
		self.id = dictionary['id']
		self.name = dictionary['name']

	def wrap_for_editing(self, pool):
		return Editor(self, pool)

	def subscribe(self, subscriber):
		"""Let event know whom to notify if it's triggered."""
		self.subscribers.append(subscriber)

	def trigger(self):
		"""Signifies that an event has happened."""
		for subscriber in self.subscribers:
			subscriber.notify(self)

	def __repr__(self):
		return self.name
