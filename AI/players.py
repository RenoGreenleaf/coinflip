from coinflip.protocols import Event
from AI.pieces import Conjunction, Option


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
