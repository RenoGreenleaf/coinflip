from random import randint


class Player:
	def __init__(self, world):
		self.world = world

	def process(self, event):
		input('> ')
		print(self.world)


class AI:
	def __init__(self, world):
		self.world = world

	def process(self, event):
		offset = randint(1, 4)
		self.world.select(offset)


class Event:
	def __init__(self):
		self.subscribers = set()

	def subscribe(self, subscriber):
		self.subscribers.add(subscriber)

	def trigger(self):
		for subscriber in self.subscribers:
			subscriber.process(self)


class Option:
	def load(self, json, relationships):
		self.description = json['description']
		self.message = json['message']
		self.pattern = json['pattern']

	def save(self):
		return {
			'description': self.description,
			'message': self.message,
			'pattern': self.pattern
		}

	def matches(self, text):
		return self.pattern == text

	def __repr__(self):
		return self.description


class World:
	"""Majority of game objects reside here."""
	def load(self, json, relationships):
		self.shown = []
		self.hidden = []

		for raw_option in json['available']:
			option = Option()
			option.load(raw_option, None)
			self.shown.append(option)

		for raw_option in json['hidden']:
			option = Option()
			option.load(raw_option, None)
			self.hidden.append(option)

	def __repr__(self):
		options = [str(option) for option in self.shown]
		return "\n".join(options)

	def select(self, offset):
		pass
