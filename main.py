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


class World:
	"""Majority of game objects reside here."""
	def load(self, json, relationships):
		self.messages = [
			'Hello, world!',
			'Bugoga!',
			'Uaaaaaaaaa!',
			'Bye!'
		]
		self.current = 0

	def __repr__(self):
		return self.messages[self.current]

	def select(self, offset):
		self.current = offset - 1
