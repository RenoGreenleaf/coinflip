# Copyright (C) 2026  Reno Greenleaf
from protocols import Event, Player


class System:
	"""A player making decisions using system input/output."""

	def __init__(self, world):
		"""Define initial properties to be sure they're available later."""
		self.world = world

	def process(self, event: Event):
		options = list(self._get_options())

		for index, option in enumerate(options):
			print(f"{index + 1}. {option.description}")

		offset = input('> ')

		if offset == 'exit':
			exit()

		option = options[int(offset) - 1]
		self.world.select(option)
		print(option.message)

	def load(self, raw: dict, relationships: dict):
		"""Implement persistent interface."""

	def save(self):
		"""Implement persistent interface."""
		return {}

	def _get_description(self):
		descriptions = []
		offset = 0

		for option in self._get_options():
			offset += 1
			descriptions.append(str(offset) + ". " + option.description)

		return "\n".join(descriptions)

	def _get_options(self):
		for option in self.world.children:
			if not option.hidden:
				yield option


class AI:
	"""A player reacting to actual players actions."""

	def __init__(self, world):
		"""Define initial properties to be sure they're available later."""
		self.world = world
		self.connections = {}
		self.nodes = {}  # inner relationships

	def process(self, event: Event):
		for node, input_ in self.connections.get(event, []):
			node.act(input_)

	def load(self, raw: dict, relationships: dict):
		for identifier, raw_node in raw['ai']['nodes'].items():
			self._obtain_node(identifier, relationships, raw_node['type'])

		for connection in raw['ai']['connections']:
			event = self.nodes[connection['trigger']]
			node = self.nodes[connection['affected']]
			input_ = connection['input']
			self.connections.setdefault(event, []).append((node, input_))

			event.subscribe(self)

	def save(self):
		return {}

	def _obtain_node(self, identifier, relationships, type_):
		if type_ == 'option':
			option = relationships[identifier]
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

	def act(self, input_: int):
		self.option.hidden = not bool(input_)

	def subscribe(self, player: Player):
		self.event.subscribe(player)

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

	def act(self, input_: int):
		if input_ == 0:
			self.a = True
		else:
			self.b = True

		if self.a and self.b:
			self.trigger()

	def subscribe(self, player: Player):
		self.subscribers.add(player)

	def trigger(self):
		for subscriber in self.subscribers:
			subscriber.process(self)

	def __hash__(self):
		return hash(id(self))
