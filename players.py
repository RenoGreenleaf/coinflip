# Copyright (C) 2026  Reno Greenleaf

class System:
	"""A player making decisions using system input/output."""

	def __init__(self, world):
		"""Define initial properties to be sure they're available later."""
		self.world = world

	def process(self, event):
		print(self.world.description)
		offset = input('> ')

		if offset == 'exit':
			exit()

		self.world.select(offset)
		print(self.world.message)

	def load(self, json, relationships):
		"""Implement persistent interface."""

	def save(self):
		"""Implement persistent interface."""
		return {}


class AI:
	"""A player reacting to actual players actions."""

	def __init__(self, world):
		"""Define initial properties to be sure they're available later."""
		self.world = world
		self.connections = {}
		self.nodes = {}  # inner relationships

	def process(self, event):
		for node, input_ in self.connections.get(event, []):
			node.act(input_)

	def load(self, json, relationships):
		for identifier, raw_node in json['ai']['nodes'].items():
			self._obtain_node(identifier, relationships, raw_node['type'])

		for connection in json['ai']['connections']:
			event = self.nodes[connection['trigger']]
			node = self.nodes[connection['affected']]
			input_ = connection['input']
			self.connections.setdefault(event, []).append((node, input_))

			event.subscribe(self)

	def save(self):
		return {}

	def _obtain_node(self, identifier, relationships, type_):
		if type_ == 'option':
			option = relationships.get('option', identifier)
			self.nodes.setdefault(identifier, Option(option, option))
		elif type_ == 'conjunction':
			self.nodes.setdefault(identifier, Conjunction())
		else:
			raise TypeError()

		return self.nodes[identifier]


class Option:
	def __init__(self, option, event):
		self.option = option
		self.event = event

	def act(self, input_):
		self.option.hidden = not bool(input_)

	def subscribe(self, subscriber):
		self.event.subscribe(subscriber)

	def trigger(self):
		self.event.trigger()

	def __hash__(self):
		return hash(self.option)

	def __eq__(self, other):
		return self.option is other


class Conjunction:
	def __init__(self):
		self.a = False
		self.b = False
		self.subscribers = set()

	def act(self, input_):
		if input_ == 0:
			self.a = True
		else:
			self.b = True

		if self.a and self.b:
			self.trigger()

	def subscribe(self, subscriber):
		self.subscribers.add(subscriber)

	def trigger(self):
		for subscriber in self.subscribers:
			subscriber.process(self)

	def __hash__(self):
		return hash(id(self))
