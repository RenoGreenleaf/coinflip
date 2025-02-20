class Event:
	"""A message broadcasted when something happens.
	Helps to interact between decoupled parts of an app."""
	def __init__(self, name):
		self.subscribers = []
		self.name = name

	def subscribe(self, subscriber):
		"""Let event know whom to notify if it's triggered."""
		self.subscribers.append(subscriber)

	def trigger(self):
		for subscriber in self.subscribers:
			subscriber.notify(self)

	def serialize(self):
		return self.name


class Irrelevant(Event):
	"""Empty event, it supposed to be triggered by default."""
	def subscribe(self, subscriber):
		pass

	def trigger(self):
		pass
