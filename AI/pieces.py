from coinflip.protocols import Player


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
