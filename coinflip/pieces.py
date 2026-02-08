from coinflip.protocols import Player


class Piece:
	"""
	Implements all interfaces for any player might need from a piece.

	So that various piece types don't need to do it again
	and only have to implement what is relevant for them.
	"""

	def __init__(self):
		self.subscribers = set()
		self.children = []

	def load(self, raw: dict, relationships: dict):
		for identifier, raw_child in raw.get('children', {}).items():
			type_ = raw_child.get('type', 'piece')
			child = self.instantiate_child(type_)
			relationships[identifier] = child
			child.load(raw_child, relationships)
			self.children.append(child)

	def save(self):
		return {}

	def act(self, input_: int):
		pass

	def instantiate_child(self, type_: str):
		from terminal.pieces import Option  # prevents circular imports

		mapping = {
			'option': Option,
			'piece': Piece,
		}
		return mapping[type_]()

	def subscribe(self, player: Player):
		self.subscribers.add(player)

	def trigger(self):
		for subscriber in self.subscribers:
			subscriber.process(self)

	def __hash__(self):
		"""Make it usable as dictionary key."""
		return hash(id(self))


class World(Piece):
	"""Majority of game objects reside here."""

	def __init__(self):
		"""Define initial properties to be sure they're available later."""
		super().__init__()
		self.selected = Piece()

	def select(self, piece):
		self.selected = piece

		if not self.selected.permanent:
			self.selected.hidden = True

		self.selected.trigger()


class Event(Piece):
	"""
	Special case, this one is outside a board.

	Represents a turn or a time tick.
	"""
