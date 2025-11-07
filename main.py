from random import randint


class Player:
	def __init__(self, world):
		self.world = world

	def process(self, event):
		offset = input('> ')
		print(self.world.select(int(offset)).message)


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

	def __init__(self):
		self.description = ""
		self.message = ""
		self.pattern = ""

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
	def __init__(self):
		self.shown = {}
		self.hidden = {}

	def load(self, json, relationships):
		for identifier, raw_option in json['available'].items():
			option = Option()
			option.load(raw_option, relationships)
			self.shown[identifier] = option

		for identifier, raw_option in json['hidden'].items():
			option = Option()
			option.load(raw_option, relationships)
			self.hidden[identifier] = option

	def __repr__(self):
		options = [str(option) for option in self.shown]
		return "\n".join(options)

	def select(self, offset):
		return self.shown[offset - 1]

	def get(self, key, identifier):
		if key != 'option':
			raise Exception()

		return self.shown.get(
			identifier,
			self.hidden.get(identifier, Option())
		)

	def unid(self, key):
		if key != 'option':
			raise Exception()

		self.shown = list(self.shown.values())
		self.hidden = list(self.hidden.values())
