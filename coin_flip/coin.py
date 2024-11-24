from scene.prop import Prop
from random import choice


class Coin(Prop):
	def __init__(self, triggers):
		self.triggers = triggers
		self.side = 'heads'

	def flip(self):
		self.side = choice(['tails', 'heads'])
		return self.side

	def describe(self, events, cli):
		cli.print(f"A coin is lying on the floor, {self.side} up.\n")

	def use(self, events, cli):
		cli.print("Playing coin flip.")
		self.triggers.trigger()
