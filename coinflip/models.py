from random import choice
from reusables.models import Scene
from reusables import nulls
from coinflip.editor import Editor
from coinflip.player import Player


class CoinFlip(Scene):
	def __init__(self):
		self.id = 0
		self.victory_threshold = 3
		self.won_event = nulls.event

		self.my_score = 0
		self.opponents_score = 0

	def save(self):
		return {
			'id': self.id,
			'type': 'coinflip',
			'victory_threshold': self.victory_threshold,
			'won_event': self.won_event.id
		}

	def load(self, dictionary, pool):
		self.id = dictionary['id']
		self.victory_threshold = dictionary['victory_threshold']
		self.won_event = pool.get_event(dictionary['won_event'])

	def flip(self, preference):
		self.side = choice(['tails', 'heads'])

		if preference == self.side:
			self.my_score += 1
		else:
			self.opponents_score += 1

		if self.is_victory():
			self.won_event.trigger()

	def is_victory(self):
		return self.my_score - self.opponents_score >= self.victory_threshold

	def wrap_for_editing(self, pool):
		return Editor(self, pool)

	def wrap_for_playing(self, pool):
		return Player(self, pool)

	def set_threshold(self, threshold):
		self.victory_threshold = threshold

	def __repr__(self):
		return f"CoinFlip (triggers {self.won_event} after {self.victory_threshold} wins)"