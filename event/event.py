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