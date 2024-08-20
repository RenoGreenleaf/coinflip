class Event:
	"""A message sent when something happens.
	Helps to interact between decoupled parts of an app."""
	def __init__(self):
		self.subscribers = []

	def subscribe(self, subscriber):
		self.subscribers.append(subscriber)

	def trigger(self):
		for subscriber in self.subscribers:
			subscriber.notify(self)


class Irrelevant(Event):
	"""Empty event, it supposed to be triggered by default."""
	
	def subscribe(self, subscriber):
		pass

	def trigger(self):
		pass