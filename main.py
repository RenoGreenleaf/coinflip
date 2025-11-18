class Player:
	def __init__(self, world):
		self.world = world

	def process(self, event):
		print(self.world.description)
		offset = input('> ')

		if offset == 'exit':
			exit()

		self.world.select(offset)
		print(self.world.message)

	def load(self, json, relationships):
		pass

	def save(self):
		return {}


class AI:
	def __init__(self, world):
		self.world = world
		self.events = {}

	def process(self, event):
		if event == self.events['syberia']:
			self.world.show(self.syberia2)
		elif event == self.events['syberia2']:
			self.world.show(self.other)

	def load(self, json, relationships):
		for name, identifier in json['ai']['variables'].items():
			setattr(self, name, relationships.get('option', identifier))

		for name, identifier in json['ai']['events'].items():
			event = relationships.get('event', identifier)
			self.events[name] = event
			event.subscribe(self)

	def save(self):
		return {}


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
		self.permanent = False
		self.subscribers = set()

	def load(self, json, relationships):
		self.description = json['description']
		self.message = json['message']
		self.permanent = json['permanent']

	def save(self):
		return {
			'description': self.description,
			'message': self.message,
			'permanent': self.permanent,
		}

	def subscribe(self, subscriber):
		self.subscribers.add(subscriber)

	def trigger(self):
		for subscriber in self.subscribers:
			subscriber.process(self)


class World:
	"""Majority of game objects reside here."""
	def __init__(self):
		self.shown = {}
		self.hidden = {}
		self.selected = Option()
		self.cleared = False

	def load(self, json, relationships):
		for identifier, raw_option in json['available'].items():
			option = Option()
			option.load(raw_option, relationships)
			self.shown[identifier] = option

		for identifier, raw_option in json['hidden'].items():
			option = Option()
			option.load(raw_option, relationships)
			self.hidden[identifier] = option

	def save(self):
		return {}

	def hide(self, option):
		index = self.shown.index(option)
		self.shown.pop(index)
		self.hidden.append(option)

	def show(self, option):
		index = self.hidden.index(option)
		self.hidden.pop(index)
		self.shown.append(option)

	def select(self, offset):
		self.selected = self.shown[int(offset) - 1]

		if not self.selected.permanent:
			self.hide(self.selected)

		self.selected.trigger()

	def get(self, key, identifier):
		if key != 'option' and key != 'event':
			raise Exception()

		return self.shown.get(
			identifier,
			self.hidden.get(identifier, Option())
		)

	def unid(self, key):
		if key != 'option' and key != 'event':
			raise Exception()

		if not self.cleared:
			self.shown = list(self.shown.values())
			self.hidden = list(self.hidden.values())
			self.cleared = True

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
