from random import choice


class Coin:
	def flip(self):
		return choice(['tails', 'heads'])
