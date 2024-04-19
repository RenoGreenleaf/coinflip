from prop import Prop
from random import choice


class Lock(Prop):
	def prepare(self):
		self.position = 0
		self.pins = []

		for pin in range(4):
			self.pins.append(choice([True, False]))

	def turn(self, is_clockwise):
		if self.pins[self.position] == is_clockwise:
			self.position += 1
			return True
		else:
			self.position = 0
			return False

	def unlocked(self):
		return self.position == len(self.pins)


class Collection(Prop):
	def __init__(self):
		self.reusable = Lock()

	def prepare(self):
		self.reusable.prepare()

	def pull(self):
		if self.reusable.unlocked():
			self.reusable.prepare()

		return self.reusable