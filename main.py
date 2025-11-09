class Player:
	def __init__(self, world):
		self.world = world

	def process(self, event):
		print(self.world.description)
		offset = input('> ')
		self.world.select(offset)
		print(self.world.message)


class AI:
	def __init__(self, world):
		self.world = world

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
		self.selected = Option()

	def load(self, json, relationships):
		for identifier, raw_option in json['available'].items():
			option = Option()
			option.load(raw_option, relationships)
			self.shown[identifier] = option

		for identifier, raw_option in json['hidden'].items():
			option = Option()
			option.load(raw_option, relationships)
			self.hidden[identifier] = option

	def select(self, offset):
		self.selected = self.shown[int(offset) - 1]

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

	def __getattribute__(self, name):
		if name == 'message':
			return self.selected.message
		elif name == 'description':
			return self._get_description()
		else:
			return super().__getattribute__(name)

	def _get_description(self):
		descriptions = []
		offset = 0

		for option in self.shown:
			offset += 1
			descriptions.append(str(offset) + ". " + option.description)

		return "\n".join(descriptions)
