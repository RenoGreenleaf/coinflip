class Player:
	def process(self, event):
		pass


class AI:
	def process(self, event):
		pass


class Event:
	def __init__(self):
		self.subscribers = set()

	def subscribe(self, subscriber):
		self.subscribers.add(subscriber)

	def trigger(self):
		for subscriber in self.subscribers:
			subscriber.process(self)


class World:
	"""Majority of game objects reside here."""

	def __init__(self):
		self.callbacks = {}
		self.options = {}
		self.hidden = {}

	def save(self):
		return {}

	def load(self, json, relationships):
		self.callbacks = {
			'hide': self._hide,
			'show': self._show
		}

		for key, option in self.options.items():
			option.load(json['available'][key], relationships)

		for key, option in self.hidden.items():
			option.load(json['hidden'][key], relationships)

	def set(self, key, identifier, value):
		if key == 'callback':
			self.callbacks[identifier] = value
		else:
			raise Exception("The key isn't supported.")

	def get(self, key, identifier):
		if key == 'callback':
			return self.callbacks[identifier]
		elif key == 'option':
			return self.options.get(identifier, self.hidden.get(identifier))
		else:
			raise Exception("The key isn't supported.")

	def unid(self):
		self.options = list(self.options.values())
		self.hidden = list(self.hidden.values())
		del self.callbacks

	def _hide(self, options):
		for option in options:
			self.options.remove(option)
			self.hidden.append(option)

	def _show(self, options):
		for option in options:
			self.hidden.remove(option)
			self.options.append(option)

	def _print(self, text):
		if text != "":
			print(text)
